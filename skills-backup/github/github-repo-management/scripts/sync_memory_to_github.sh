#!/usr/bin/env bash
set -euo pipefail

SOURCE_DIR="$HOME/.hermes/memories"
VAULT_DIR="$HOME/.hermes/vault/memories"
REPO_DIR="$HOME/.hermes/vault"
LOG_FILE="$HOME/.hermes/logs/github_sync.log"

# Ensure log dir exists
mkdir -p "$(dirname "$LOG_FILE")"

{
    echo "[$(date -u +"%Y-%m-%dT%H:%M:%SZ")] Starting memory sync..."
    
    # Ensure vault dir exists
    mkdir -p "$VAULT_DIR"

    # Copy files (overwrite)
    cp -r "$SOURCE_DIR"/* "$VAULT_DIR"/

    cd "$REPO_DIR"

    # Configure git user if not set (should already be)
    git config user.name "${GIT_AUTHOR_NAME:-Hermes Agent}"
    git config user.email "${GIT_AUTHOR_EMAIL:-hermes@local}"

    # Add all changes
    git add .

    # Check if there are changes to commit
    if ! git diff-index --quiet HEAD --; then
        TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
        git commit -m "Sync memory files: $TIMESTAMP"
        git push origin main
        echo "[$(date -u +"%Y-%m-%dT%H:%M:%SZ")] Synced changes to GitHub."
    else
        echo "[$(date -u +"%Y-%m-%dT%H:%M:%SZ")] No changes to sync."
    fi
} >> "$LOG_FILE" 2>&1