---
name: social-media-api
description: "Fetch recent posts from X (Twitter) and post them to a Slack channel. Useful for news updates, monitoring, or automated reporting."
version: 1.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
tags: [social-media, x-api, twitter, news]
---

# Social Media API Skill

## Overview
This skill automates the retrieval of recent posts from X (formerly Twitter) using the X API v2 and posts a summary to a specified Slack channel. It can be scheduled via cron or triggered manually.

## Prerequisites
- X API bearer token (obtain from X developer portal). Store it in the `.env` file as `X_API_BEARER_TOKEN`.
- Slack bot token with `chat:write` scope. Store as `SLACK_BOT_TOKEN` in `.env`.
- Hermes Agent installed and configured with Slack integration.

## Steps
1. **Set up environment variables**:
   ```bash
   export X_API_BEARER_TOKEN=your_x_token
   export SLACK_BOT_TOKEN=your_slack_token
   ```
2. **Create a Slack channel** (e.g., `#genai-newsflash`) where the posts will be posted.
3. **Run the skill manually** (optional):
   ```bash
   hermes skill run social-media-api --channel "#genai-newsflash"
   ```
4. **Schedule daily runs** using cron:
   ```cron
   0 8 * * * hermes skill run social-media-api --channel "#genai-newsflash"
   ```

## Commands
- `hermes skill run social-media-api [--channel "#channel"]` – Execute the skill once.
- `hermes skill list` – List installed skills.

## Pitfalls
- **Missing API token**: The skill will fail with a 401 error. Ensure `X_API_BEARER_TOKEN` is set.
- **Rate limits**: X API enforces rate limits; if you exceed them, the skill will pause. Monitor the logs.
- **Slack token scopes**: Ensure the bot token includes `chat:write` and `chat:write.public` if posting to public channels.

## Verification
After running, check the Slack channel for the posted message. If missing, inspect `~/.hermes/logs/gateway.log` for errors.

## References
- X API v2 documentation: https://developer.x.com/en/docs/twitter-api
- Slack API docs: https://api.slack.com/methods/chat.postMessage