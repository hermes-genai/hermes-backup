---
name: slack-proactive-engagement
description: Enables Hermes to proactively engage in Slack conversations with helpful, kawaii-style interactions
category: software-development
---

# Slack Proactive Engagement Skill

This skill enables Hermes to proactively engage in Slack conversations by:
1. Monitoring recent messages in channels
2. Detecting when to jump in (questions, help requests, or appropriate moments for humor)
3. Generating contextual responses with the kawaii personality
4. Posting engaging messages to keep conversations lively

## Trigger Conditions
- When deployed as a cron job or manual trigger
- When monitoring Slack channels for engagement opportunities
- When the bot should proactively help or entertain

## Steps
1. **Monitor Channel Activity** (if implemented with real-time listening)
   - Or fetch recent messages from Slack API
   - Look for questions, help requests, or lulls in conversation

2. **Analyze Context**
   - Determine if intervention is helpful
   - Identify tone and topic of conversation
   - Check if someone needs assistance

3. **Generate Response**
   - Use kawaii personality: cute expressions, enthusiasm, ~!, ^_^, desu~
   - Be helpful, friendly, and slightly playful
   - Keep responses brief but meaningful
   - Optionally add relevant facts, jokes, or encouragement

4. **Post to Slack**
   - Use send_message tool to post to appropriate channel
   - Target: usually 'slack:general' or specific channels as configured

## Configuration
- Requires Slack integration to be set up
- Works best when require_mention is false in Slack config
- Can be tuned with specific channels for engagement

## Example Engagement Types
- Answering questions that appear in channels
- Offering help when someone seems stuck
- Sharing interesting AI facts or news
- Light-hearted jokes or puns
- Encouraging messages during long discussions
- Welcoming new participants

## Safety Notes
- Avoid interrupting serious discussions unless clearly helpful
- Don't spam - wait for appropriate moments
- Respect channel topics and purposes
- Keep content work-appropriate and inclusive

## Troubleshooting (Direct Action - User Preferred)
Follow these steps in order - test after each step:

1. **Verify bot in channel & basic messaging**:
   - `/invite @hermes-bot` in target channel
   - `hermes send_message -t slack:#channel -m "test"` 
   - If this fails, stop here - fix basic messaging first

2. **Check Slack configuration** (only if basic messaging works):
   - `hermes config get slack.require_mention` (should be false)
   - `hermes config get slack.free_response_channels` (should include your channel)
   - If wrong: `hermes config set slack.require_mention false` and/or `hermes config set slack.free_response_channels "general-nemotron-fast,genai-newsflash,genai-research,reasoning-nemotron-super-120b"`
   - Then: `hermes gateway restart`

3. **Verify cron job execution**:
   - `hermes cron list` (check last_run_at and last_status for your proactive job)
   - If not running: `hermes cron run <job_id>` to test manually

4. **Check skill execution**:
   - Review logs: `grep -i "slack-proactive-engagement" ~/.hermes/logs/gateway.log | tail -10`

**User Preference**: Each step includes immediate verification commands. Stop and fix at the first step that fails - don't proceed to theoretical explanations until basic functionality works.

## Usage
This skill is designed to be called periodically (e.g., via cronjob) or triggered manually when proactive engagement is desired.