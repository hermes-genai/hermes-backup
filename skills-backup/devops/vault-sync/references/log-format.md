# Vault Synchronization Log Format

Each line in the log file (`~/.hermes/logs/vault_sync.log`) is prefixed with a timestamp in ISO 8601 UTC format (e.g., `[2026-05-14T16:34:46Z]`).

## Log Entries

- `Starting vault sync...` — Indicates the beginning of a synchronization run.
- `Synced: <item>` — Successfully copied or synchronized the item (SOUL.md, memories/, config.yaml, plans/, skills/).
- `WARNING: Source not found: <item>` — The source item does not exist; skipped.
- `Synced changes to GitHub.` — Changes were committed and pushed to the remote repository.
- `No changes to sync.` — The vault repository is up-to-date; no commit performed.

## Error Messages

- `cp: cannot create regular file ...: Not a directory` — Indicates an outdated script that attempted to copy a directory as a file. Fixed in version 1.0.0+ by using `rsync` for directories.
- `rsync: [sender] change_dir ... failed: Not a directory` — Indicates a misconfiguration where a file was listed as a directory in the `ITEMS` array (or vice versa).
- Git authentication errors — Check that `git config user.name` and `user.email` are set and that you have push access to the repository.

## Example

```
[2026-05-14T16:34:46Z] Starting vault sync...
  Synced: SOUL.md
  Synced: memories/
  Synced: config.yaml
  Synced: plans/
  Synced: skills/
[main f072e10] Vault sync: "2026-05-14T16:34:46Z"
  1 file changed, 17 insertions(+), 4 deletions(-)
To https://github.com/hermes-genai/hermes-vault.git
   ddbfb01..f072e10  main -> main
[2026-05-14T16:34:47Z] Synced changes to GitHub.
```