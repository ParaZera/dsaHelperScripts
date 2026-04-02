#!/bin/bash
set -euo pipefail

# Shared installer for Claude Code agent tooling.
# Run as root. Pass the non-root username via CLAUDE_USER env var.
#
# Installs: zsh, fzf, fd, rg, iptables/ipset (firewall), gh, glab,
#           git-delta, Claude Code CLI, zsh-in-docker, firewall sudoers.
#
# Usage in Dockerfile:
#   COPY shared/install-claude-tools.sh /tmp/
#   COPY shared/init-firewall.sh /usr/local/bin/
#   RUN CLAUDE_USER=yocto GLAB_VERSION=1.82.0 /tmp/install-claude-tools.sh

CLAUDE_USER=${CLAUDE_USER:?CLAUDE_USER must be set}
GLAB_VERSION=${GLAB_VERSION:-1.82.0}
GIT_DELTA_VERSION=${GIT_DELTA_VERSION:-0.18.2}
CLAUDE_CODE_VERSION=${CLAUDE_CODE_VERSION:-latest}
ZSH_IN_DOCKER_VERSION=${ZSH_IN_DOCKER_VERSION:-1.2.0}

ARCH=$(dpkg --print-architecture)
HOME_DIR=$(eval echo "~${CLAUDE_USER}")

echo "=== Installing Claude Code agent tools for user '${CLAUDE_USER}' ==="

# --- APT packages ---
apt-get update && apt-get install -y --no-install-recommends \
    zsh \
    fzf \
    fd-find \
    ripgrep \
    iptables \
    ipset \
    iproute2 \
    dnsutils \
    aggregate \
    jq \
    less \
    man-db \
    gh \
    nano \
    && rm -rf /var/lib/apt/lists/*

# fd-find installs as "fdfind", symlink to "fd"
ln -sf /usr/bin/fdfind /usr/local/bin/fd

# --- GitLab CLI (glab) ---
wget -q "https://gitlab.com/gitlab-org/cli/-/releases/v${GLAB_VERSION}/downloads/glab_${GLAB_VERSION}_linux_${ARCH}.deb"
dpkg -i "glab_${GLAB_VERSION}_linux_${ARCH}.deb"
rm "glab_${GLAB_VERSION}_linux_${ARCH}.deb"

# --- git-delta ---
wget -q "https://github.com/dandavison/delta/releases/download/${GIT_DELTA_VERSION}/git-delta_${GIT_DELTA_VERSION}_${ARCH}.deb"
dpkg -i "git-delta_${GIT_DELTA_VERSION}_${ARCH}.deb"
rm "git-delta_${GIT_DELTA_VERSION}_${ARCH}.deb"

# --- npm global prefix (user-writable, no sudo needed for npm -g) ---
mkdir -p /usr/local/share/npm-global
chown -R "${CLAUDE_USER}:${CLAUDE_USER}" /usr/local/share/npm-global

# --- Claude Code CLI ---
runuser -u "${CLAUDE_USER}" -- \
    env NPM_CONFIG_PREFIX=/usr/local/share/npm-global \
    npm install -g "@anthropic-ai/claude-code@${CLAUDE_CODE_VERSION}"

# --- Command history persistence ---
mkdir -p /commandhistory
touch /commandhistory/.bash_history
chown -R "${CLAUDE_USER}:${CLAUDE_USER}" /commandhistory

# --- Claude config directory ---
mkdir -p "${HOME_DIR}/.claude"
chown -R "${CLAUDE_USER}:${CLAUDE_USER}" "${HOME_DIR}/.claude"

# --- zsh-in-docker (Oh My Zsh + Powerlevel10k) ---
runuser -u "${CLAUDE_USER}" -- sh -c \
    "$(wget -O- https://github.com/deluan/zsh-in-docker/releases/download/v${ZSH_IN_DOCKER_VERSION}/zsh-in-docker.sh)" -- \
    -p git \
    -p fzf \
    -a "export PROMPT_COMMAND='history -a' && export HISTFILE=/commandhistory/.bash_history" \
    -x

# --- Firewall sudoers (assumes init-firewall.sh is already at /usr/local/bin/) ---
chmod +x /usr/local/bin/init-firewall.sh
echo "${CLAUDE_USER} ALL=(root) NOPASSWD: /usr/local/bin/init-firewall.sh" > "/etc/sudoers.d/${CLAUDE_USER}-firewall"
chmod 0440 "/etc/sudoers.d/${CLAUDE_USER}-firewall"

echo "=== Claude Code agent tools installed ==="
