---
name: vault-sync
description: "Synchronize Hermes vault (memories, config, plans, skills) to private GitHub repository."
version: 1.0.1
author: Hermes Agent
license: MIT
platforms:
  - linux
  - macos
metadata:
  hermes:
    tags: [backup, sync, vault, github, repository]
    related_skills: [github-repo-management, cronjob]
---

# Vault Synchronization Skill

Automatically backs up Hermes agent's vault directory to a private GitHub repository. This includes memories (MEMORY.md, USER.md), configuration files, plans, skills, and SOUL.md.

## Overview

The vault synchronization process:
1. Copies/syncs specified files and directories from `~/.hermes/` to `~/.hermes/vault/`
2. Commits changes to the local git repository only if there are differences
3. Pushes to the remote GitHub repository (configured as origin)
4. Logs each sync operation with timestamps

## What Gets Synced

By default, the following items are synchronized:
- `SOUL.md` - Agent's personality and operational guidelines
- `memories/` - Persistent memory (MEMORY.md, USER.md)
- `config.yaml` - Agent configuration
- `plans/` - Saved implementation plans
- `skills/` - Custom skills and skill libraries

## The Synchronization Script

The core synchronization logic is included in this skill at `scripts/sync_vault.sh`:

```bash
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

## Key Features

- **Efficient Directory Sync**: Uses `rsync -av --delete` for directories to properly handle file additions, modifications, and deletions
- **Change-Detection**: Only commits and pushes when there are actual changes
- **Logging**: Detailed logs with timestamps in `~/.hermes/logs/vault_sync.log`
- **Safe Operations**: Uses `set -euo pipefail` for robust error handling
- **Git User Configuration**: Automatically sets git user from environment variables or defaults

## Setup Instructions

### 1. Prepare the Vault Repository

If you haven't already set up the vault repository:

```bash
# Initialize vault directory as git repo
cd ~/.hermes
mkdir -p vault
cd vault
git init

# Add remote (replace with your actual repository URL)
git remote add origin https://github.com/your-username/hermes-vault.git
git branch -M main

# Create initial commit if needed
touch .gitignore
git add .gitignore
git commit -m "Initial vault commit"
```

### 2. Configure Git Credentials

Set up authentication for pushing to GitHub:

```bash
# Option 1: Use GitHub CLI (recommended)
gh auth login

# Option 2: Set environment variables
export GIT_AUTHOR_NAME="Your Name"
export GIT_AUTHOR_EMAIL="your.email@example.com"
export GITHUB_TOKEN="your_github_pat"  # For API operations if needed

# Option 3: Configure git credentials helper
git config --global credential.helper store
```

### 3. Make the Script Executable

```bash
chmod +x ~/.hermes/scripts/sync_vault.sh
```

## Usage

### Manual Sync

```bash
~/.hermes/scripts/sync_vault.sh
```

### Automated Sync with Cron

To set up automatic synchronization (e.g., every 30 minutes):

```bash
# Edit crontab
crontab -e

# Add line for every 30 minutes
*/30 * * * * /home/hermes/.hermes/scripts/sync_vault.sh
```

Or using the Hermes cronjob tool:

```bash
hermes cronjob create \
  --name "vault-sync" \
  --schedule "*/30 * * * *" \
  --prompt "Run vault synchronization script" \
  --skills "[]" \
  --workdir "/home/hermes"
```

## Troubleshooting

### Common Issues

1. **Permission Errors**
   - Ensure the script is executable: `chmod +x ~/.hermes/scripts/sync_vault.sh`
   - Check that you have write permissions to the vault directory and GitHub repo

2. **Git Authentication Failures**
   - Verify GitHub authentication is working: `gh auth status`
   - Check that git user is properly configured: `git config user.name` and `git config user.email`

3. **No Changes Detected**
   - Check the log file: `cat ~/.hermes/logs/vault_sync.log`
   - Verify source files exist and are readable
   - Ensure the vault directory is a valid git repository

4. **Directory Sync Issues**
   - The script uses `rsync -av --delete` for directories to ensure proper synchronization
   - This handles file deletions in source (removes them from destination)
   - Preserves file permissions, timestamps, and symbolic links

5. **Directory/File Conflict Errors**
   - If you see errors like `cp: cannot create regular file '<path>/plans//': Not a directory`, it indicates a mismatch where the source is a directory but the destination exists as a file (or vice versa).
   - The sync script now includes pre-sync checks to remove conflicting file types before syncing/copying (see lines 34-36 and 42-43 in `scripts/sync_vault.sh`).
   - This issue was resolved in vault-sync skill version 1.0.1.

## Best Practices

- **Regular Monitoring**: Check the sync log periodically to ensure backups are working
- **Token Security**: If using GitHub PAT, store it securely and never commit it to the repository
- **Branch Strategy**: Consider using a dedicated branch for automated syncs if you also manually commit to the vault
- **Retention**: Git history provides versioning - you can recover previous states if needed
- **Selective Sync**: Modify the `ITEMS` array in the script if you need to sync additional or different directories

## Related Skills

- `github-repo-management`: For advanced GitHub repository operations
- `cronjob`: For scheduling automated synchronizations
- `github-auth`: For setting up GitHub authentication

## Change Log

- **1.0.1**: Enhanced directory/file conflict resolution
  - Added pre-sync checks to handle cases where source and destination
    types mismatch (e.g., source is directory but destination exists as file)
  - Now removes conflicting file types before syncing/copying

- **1.0.0**: Initial release with rsync-based directory synchronization
  - Fixed directory handling issues that caused "Not a directory" errors
  - Improved reliability of plans/ and skills/ directory synchronization
  - Added comprehensive logging and error handling