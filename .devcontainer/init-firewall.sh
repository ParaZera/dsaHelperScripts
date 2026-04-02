#!/bin/bash
set -euo pipefail
IFS=$'\n\t'

# Firewall for Claude Code devcontainer
# Based on Anthropic's reference implementation, extended for GitLab + SSH access.
#
# What's allowed:
#   - DNS (udp/53)
#   - SSH (tcp/22) — for GitLab, remote dev-devices, etc.
#   - Localhost
#   - Host network (VSCode <-> container communication)
#   - GitHub (IPs fetched dynamically from /meta)
#   - npm registry, Anthropic API, Sentry, Statsig, VSCode Marketplace
#   - Your GitLab instance (configure GITLAB_HOST below)
#
# Everything else is blocked (default-deny).

###############################################################################
# CONFIGURATION — Edit these for your environment
###############################################################################

# Your GitLab instance hostname (leave empty to skip)
GITLAB_HOST="${GITLAB_HOST:-}"
# Example: GITLAB_HOST="gitlab.example.com"

# Additional domains to allow (space-separated)
EXTRA_ALLOWED_DOMAINS="${EXTRA_ALLOWED_DOMAINS:-}"
# Example: EXTRA_ALLOWED_DOMAINS="pypi.org files.pythonhosted.org"

###############################################################################

echo "=== Initializing firewall ==="

# 1. Extract Docker DNS info BEFORE any flushing
DOCKER_DNS_RULES=$(iptables-save -t nat | grep "127\.0\.0\.11" || true)

# Flush existing rules
iptables -F
iptables -X
iptables -t nat -F
iptables -t nat -X
iptables -t mangle -F
iptables -t mangle -X
ipset destroy allowed-domains 2>/dev/null || true

# 2. Restore Docker internal DNS resolution
if [ -n "$DOCKER_DNS_RULES" ]; then
    echo "Restoring Docker DNS rules..."
    iptables -t nat -N DOCKER_OUTPUT 2>/dev/null || true
    iptables -t nat -N DOCKER_POSTROUTING 2>/dev/null || true
    echo "$DOCKER_DNS_RULES" | xargs -L 1 iptables -t nat
else
    echo "No Docker DNS rules to restore"
fi

# 3. Allow DNS, SSH, and localhost before any restrictions
iptables -A OUTPUT -p udp --dport 53 -j ACCEPT
iptables -A INPUT -p udp --sport 53 -j ACCEPT
iptables -A OUTPUT -p tcp --dport 22 -j ACCEPT
iptables -A INPUT -p tcp --sport 22 -m state --state ESTABLISHED -j ACCEPT
iptables -A INPUT -i lo -j ACCEPT
iptables -A OUTPUT -o lo -j ACCEPT

# 4. Create ipset for allowed IPs
ipset create allowed-domains hash:net

# 5. Fetch GitHub IP ranges
echo "Fetching GitHub IP ranges..."
gh_ranges=$(curl -s https://api.github.com/meta)
if [ -z "$gh_ranges" ]; then
    echo "ERROR: Failed to fetch GitHub IP ranges"
    exit 1
fi

if ! echo "$gh_ranges" | jq -e '.web and .api and .git' >/dev/null; then
    echo "ERROR: GitHub API response missing required fields"
    exit 1
fi

echo "Processing GitHub IPs..."
while read -r cidr; do
    if [[ ! "$cidr" =~ ^[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}/[0-9]{1,2}$ ]]; then
        echo "WARNING: Skipping invalid CIDR from GitHub meta: $cidr"
        continue
    fi
    ipset add allowed-domains "$cidr" 2>/dev/null || true
done < <(echo "$gh_ranges" | jq -r '(.web + .api + .git)[]' | aggregate -q)

# 6. Resolve and add standard allowed domains
ALLOWED_DOMAINS=(
    "registry.npmjs.org"
    "api.anthropic.com"
    "sentry.io"
    "statsig.anthropic.com"
    "statsig.com"
    "marketplace.visualstudio.com"
    "vscode.blob.core.windows.net"
    "update.code.visualstudio.com"
)

# Add GitLab if configured
if [ -n "$GITLAB_HOST" ]; then
    ALLOWED_DOMAINS+=("$GITLAB_HOST")
    # GitLab SaaS (gitlab.com) uses additional subdomains for git, registry, etc.
    if [ "$GITLAB_HOST" = "gitlab.com" ]; then
        ALLOWED_DOMAINS+=(
            "registry.gitlab.com"
            "storage.googleapis.com"
        )
    fi
    echo "GitLab host added: $GITLAB_HOST"
fi

# Add any extra domains
for extra in $EXTRA_ALLOWED_DOMAINS; do
    ALLOWED_DOMAINS+=("$extra")
    echo "Extra domain added: $extra"
done

for domain in "${ALLOWED_DOMAINS[@]}"; do
    echo "Resolving $domain..."
    ips=$(dig +noall +answer A "$domain" | awk '$4 == "A" {print $5}')
    if [ -z "$ips" ]; then
        echo "WARNING: Failed to resolve $domain (skipping)"
        continue
    fi
    while read -r ip; do
        if [[ "$ip" =~ ^[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}$ ]]; then
            ipset add allowed-domains "$ip" 2>/dev/null || true
            echo "  Added $ip for $domain"
        fi
    done <<< "$ips"
done

# 7. Allow host network (VSCode <-> container)
HOST_IP=$(ip route | grep default | cut -d" " -f3)
if [ -z "$HOST_IP" ]; then
    echo "ERROR: Failed to detect host IP"
    exit 1
fi
HOST_NETWORK=$(echo "$HOST_IP" | sed "s/\.[0-9]*$/.0\/24/")
echo "Host network: $HOST_NETWORK"
iptables -A INPUT -s "$HOST_NETWORK" -j ACCEPT
iptables -A OUTPUT -d "$HOST_NETWORK" -j ACCEPT

# 8. Set default policies to DROP
iptables -P INPUT DROP
iptables -P FORWARD DROP
iptables -P OUTPUT DROP

# Allow established connections
iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT
iptables -A OUTPUT -m state --state ESTABLISHED,RELATED -j ACCEPT

# Allow outbound to allowed IPs only
iptables -A OUTPUT -m set --match-set allowed-domains dst -j ACCEPT

# Reject everything else with immediate feedback
iptables -A OUTPUT -j REJECT --reject-with icmp-admin-prohibited

# 9. Verify
echo ""
echo "=== Firewall verification ==="
if curl --connect-timeout 5 https://example.com >/dev/null 2>&1; then
    echo "FAIL: Was able to reach example.com (should be blocked)"
    exit 1
else
    echo "PASS: example.com blocked"
fi

if ! curl --connect-timeout 5 https://api.github.com/zen >/dev/null 2>&1; then
    echo "FAIL: Cannot reach api.github.com (should be allowed)"
    exit 1
else
    echo "PASS: api.github.com reachable"
fi

if [ -n "$GITLAB_HOST" ]; then
    if ! curl --connect-timeout 5 "https://${GITLAB_HOST}" >/dev/null 2>&1; then
        echo "WARNING: Cannot reach ${GITLAB_HOST} — check DNS/network"
    else
        echo "PASS: ${GITLAB_HOST} reachable"
    fi
fi

echo ""
echo "=== Firewall active ==="
