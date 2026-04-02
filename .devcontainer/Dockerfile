# Python development environment with Claude Code agent
#
# Base: python:3.12-bookworm (Debian + Python + pip + uv)
# Shared: Claude Code CLI, firewall, zsh, glab, git-delta (via shared script)
#
# Self-contained: copy this directory as .devcontainer/ into any Python project.

ARG PYTHON_IMAGE=python:3.12-bookworm
FROM ${PYTHON_IMAGE}

ARG DEBIAN_FRONTEND=noninteractive
ARG TZ
ENV TZ="$TZ"

# Create non-root user "python" (UID 1000) with passwordless sudo.
RUN apt-get update && apt-get install -y --no-install-recommends sudo && \
    groupadd --gid 1000 python && \
    useradd --uid 1000 --gid 1000 -m -s /bin/zsh python && \
    echo "python ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/python-nopasswd && \
    chmod 0440 /etc/sudoers.d/python-nopasswd && \
    rm -rf /var/lib/apt/lists/*

# Node.js 20 (Claude Code needs Node 20+)
RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash - && \
    apt-get install -y --no-install-recommends nodejs && \
    rm -rf /var/lib/apt/lists/*

# uv — fast Python package/project manager (replaces pip, pip-tools, virtualenv)
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /usr/local/bin/

# Workspace
RUN mkdir -p /workdir && chown python:python /workdir

# --- Shared Claude Code agent tools ---
ARG GLAB_VERSION=1.82.0
ARG GIT_DELTA_VERSION=0.18.2
ARG CLAUDE_CODE_VERSION=latest
ARG ZSH_IN_DOCKER_VERSION=1.2.0

COPY init-firewall.sh /usr/local/bin/
COPY install-claude-tools.sh /tmp/
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
    --mount=type=cache,target=/var/lib/apt,sharing=locked \
    --mount=type=cache,target=/tmp/npm-cache,uid=1000,gid=1000 \
    CLAUDE_USER=python \
    GLAB_VERSION=${GLAB_VERSION} \
    GIT_DELTA_VERSION=${GIT_DELTA_VERSION} \
    CLAUDE_CODE_VERSION=${CLAUDE_CODE_VERSION} \
    ZSH_IN_DOCKER_VERSION=${ZSH_IN_DOCKER_VERSION} \
    npm_config_cache=/tmp/npm-cache \
    /tmp/install-claude-tools.sh && \
    rm /tmp/install-claude-tools.sh

USER python

ENV NPM_CONFIG_PREFIX=/usr/local/share/npm-global
ENV PATH=$PATH:/usr/local/share/npm-global/bin
ENV SHELL=/bin/zsh
ENV DEVCONTAINER=true

WORKDIR /workdir
