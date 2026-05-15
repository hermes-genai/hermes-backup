#!/usr/bin/env bash
set -euo pipefail

SOURCE_BASE="$HOME/.hermes"
VAULT_BASE="$HOME/.hermes/vault"
LOG_FILE="$HOME/.hermes/logs/vault_sync.log"

# Ensure log directory exists
mkdir -p "$(dirname "$LOG_FILE")"

{
    echo "[$(date -u +\"%Y-%m-%dT%H:%M:%SZ\")] Starting vault sync..."
    
    # Define what to sync (relative to SOURCE_BASE)
    declare -a ITEMS=(
        "SOUL.md"
        "memories"
        "config.yaml"
        "plans"
        "skills"
    )

    # Ensure vault base exists
    mkdir -p "$VAULT_BASE"

    for item in "${ITEMS[@]}"; do
        src="$SOURCE_BASE/$item"
        dest="$VAULT_BASE/$item"
        if [[ -e "$src" ]]; then
            # Ensure destination directory exists
            mkdir -p "$(dirname "$dest")"
            if [[ -d "$src" ]]; then
                # Use rsync to sync directory contents, preserving structure
                # First, remove destination if it's a file (to allow directory sync)
                if [[ -f "$dest" || -L "$dest" ]]; then
                    rm -f "$dest"
                fi
                rsync -av --delete "$src/" "$dest/"
            else
                # Copy file directly
                # Remove destination if it's a directory (to allow file copy)
                if [[ -d "$dest" ]]; then
                    rm -rf "$dest"
                fi
                cp "$src" "$dest"
            fi
            echo "  Synced: $item"
        else
            echo "  WARNING: Source not found: $item"
        fi
    done

    cd "$VAULT_BASE"

    # Configure git user (should be set via environment or git config)
    git config user.name "${GIT_AUTHOR_NAME:-Hermes Agent}"
    git config user.email "${GIT_AUTHOR_EMAIL:-hermes@local}"

    # Add changes
    git add .

    # Check for changes and commit if needed
    if ! git diff-index --quiet HEAD --; then
        TIMESTAMP=$(date -u +\"%Y-%m-%dT%H:%M:%SZ\")
        git commit -m "Vault sync: $TIMESTAMP"
        git push origin main
        echo "[$(date -u +\"%Y-%m-%dT%H:%M:%SZ\")] Synced changes to GitHub."
    else
        echo "[$(date -u +\"%Y-%m-%dT%H:%M:%SZ\")] No changes to sync."
    fi
} >> "$LOG_FILE" 2>&1