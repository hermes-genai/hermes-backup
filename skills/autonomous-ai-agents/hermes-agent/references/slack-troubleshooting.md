# Slack Socket Mode Troubleshooting Guide

## Common Issues and Solutions

### 1. Gateway exits immediately after starting
**Symptoms**: The Hermes gateway process starts but exits within seconds with no visible error output.

**Logs to check**: 
```bash
grep -i "slack\|socket" ~/.hermes/logs/gateway.log
```

**Typical error messages**:
- `[Slack] SLACK_APP_TOKEN not set`
- `[Slack] SLACK_BOT_TOKEN not set`
- `[Slack] Failed to start Socket Mode connection`

**Solution**:
1. Verify both tokens are present in your `.env` file:
   ```bash
   grep -E 'SLACK_BOT_TOKEN|SLACK_APP_TOKEN' ~/.hermes/.env
   ```
2. Ensure tokens have correct format:
   - `SLACK_BOT_TOKEN` should start with `xoxb-`
   - `SLACK_APP_TOKEN` should start with `xapp-`
3. Restart the gateway:
   ```bash
   hermes gateway restart
   ```

### 2. Bot appears online but doesn't respond to messages
**Symptoms**: Slack shows the bot as online, but it ignores messages in channels or DMs.

**Most Common Issue - require_mention setting**: 
The most frequent cause is `slack.require_mention: true` (the default). When enabled, the bot ONLY responds when explicitly mentioned with @botname in a channel. It will ignore regular messages in channels unless they are direct messages or the bot is mentioned.

**Quick verification for require_mention**:
1. Send a direct message to the bot (should work regardless of require_mention)
2. Try @mentioning the bot in a channel (should work if Slack permissions are correct)
3. Send a regular message in a channel without mentioning (will be ignored if require_mention is true)

**If steps 1 and 2 work but step 3 is ignored, then require_mention is the cause.**

**To fix require_mention issues**:
1. Check current setting: `hermes config get slack.require_mention`
2. If set to true and you want the bot to respond without mention:
   ```bash
   hermes config set slack.require_mention false
   hermes gateway restart
   ```
3. Alternatively, allow specific channels to respond without mention:
   ```bash
   hermes config set slack.free_response_channels "general,random"
   hermes gateway restart
   ```

**Other possible causes** (check these if require_mention is NOT the issue):
- Missing `message.channels` subscription (for public channels)
- Missing `im:read` or `im:write` scopes (for DMs)
- Bot not added to the channel
- Socket Mode connection unstable
- Missing `app_mention` event subscription (critical for responding to @mentions)

**Complete solution checklist**:
1. First check require_mention setting (as above)
2. Check Slack app configuration:
   - Go to your Slack app → OAuth & Permissions
   - Ensure Bot Token Scopes include:
     - `channels:history`
     - `channels:read`
     - `chat:write`
     - `im:history`
     - `im:read`
     - `im:write`
     - `mpim:history`
     - `reactions:read`
     - `reactions:write`
     - `app_mentions:read` (required for responding to @mentions)
3. In Socket Mode settings, ensure these event subscriptions are enabled:
   - `app_mention` (critical for responding to @mentions)
   - `message.channels`
   - `message.groups`
   - `message.im`
   - `message.mpim`
4. Verify Hermes configuration (beyond require_mention):
   - Restart gateway after config changes: `hermes gateway restart`
5. Invite the bot to the channel: `/invite @hermes-bot` (replace with your bot's name)
6. Restart the gateway after making changes

**Important**: Even when all Slack app permissions and event subscriptions are correctly configured, if `slack.require_mention` is set to `true`, the bot will NOT respond to regular channel messages. Always check this setting first when the bot appears online but ignores channel messages.

### 3. Socket Mode connection repeatedly disconnects
**Symptoms**: Gateway logs show frequent reconnect attempts or connection lost errors.

**Possible causes**:
- Network interference or firewall blocking
- Insufficient permissions on the Slack app
- Rate limiting from Slack API

**Solution**:
1. Check network connectivity to Slack's Socket Mode endpoints
2. Verify the Slack app has `connections:write` scope (required for Socket Mode)
3. Check gateway logs for rate limit warnings (`rate_limited` or `too_many_requests`)
4. Consider increasing gateway timeout if needed:
   ```bash
   hermes config set agent.gateway_timeout 3600
   hermes gateway restart
   ```

### 4. Permission denied errors when trying to post
**Symptoms**: Bot connects successfully but fails when attempting to send messages.

**Logs to check**:
```bash
grep -i "error\|failed\|denied" ~/.hermes/logs/gateway.log | grep -i "slack\|chat\|message"
```

**Typical errors**:
- `channel_not_found`
- `not_in_channel`
- `missing_scope`
- `account_inactive`

**Solution**:
1. Verify the bot is a member of the target channel
2. Check that the Bot Token has `chat:write` scope
3. For private channels, ensure the bot was invited to that specific channel
4. Test with a simple message to isolate the issue:
   ```bash
   hermes send-message -t slack:general -m "test"
   ```

## Verification Steps

After making configuration changes, follow these steps to verify the fix:

1. **Check .env file**:
   ```bash
   # Should show both tokens without comments
   grep -E '^SLACK_BOT_TOKEN=|^SLACK_APP_TOKEN=' ~/.hermes/.env
   ```

2. **Restart gateway cleanly**:
   ```bash
   hermes gateway restart
   ```

3. **Watch logs for successful connection**:
   ```bash
   # In another terminal, tail the logs
   tail -f ~/.hermes/logs/gateway.log
   ```
   Look for: `[Slack] Socket Mode connection opened`

4. **Send test message**:
   ```bash
   hermes send-message -t slack:general -m "Hermes Slack connectivity test"
   ```

## Prevention Tips

- **Keep tokens secure**: Never commit `.env` to version control
- **Regular validation**: Periodically check that tokens haven't expired
- **Monitor logs**: Set up log rotation and monitoring for the gateway
- **Test after Slack app changes**: Any modification to Slack app permissions requires gateway restart
- **Use dedicated bot user**: Consider creating a separate Slack user for the bot to avoid confusion

## Related Configuration

The Slack integration uses these configuration sections in `config.yaml`:

```yaml
slack:
  require_mention: true      # Set false to respond to all messages
  free_response_channels: '' # Comma-separated list of channels where no mention is needed
  allowed_channels: ''       # Restrict bot to specific channels (empty = all)
  channel_prompts: {}        # Custom prompts per channel
```

These can be adjusted via:
```bash
hermes config set slack.require_mention false
hermes config set slack.free_response_channels "general,random"
hermes gateway restart
```