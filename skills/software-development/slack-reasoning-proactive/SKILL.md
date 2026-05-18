---
name: slack-reasoning-proactive
description: Generate a thoughtful, reasoning-based message for Slack using the 120b model and post to a specific channel
category: software-development
---

# Slack Reasoning Proactive Skill

This skill generates a thoughtful, reasoning-based message using the NVIDIA Nemotron 3 Super 120b model and posts it to a specified Slack channel (e.g., #general-reasoning).

## Trigger Conditions
- When deployed as a cron job for periodic reasoning updates
- When manual triggering for deep thought sharing

## Steps
1. **Delegate a Subagent** with the 120b model to generate a reasoning-based message
   - Use the model: nvidia/nemotron-3-super-120b-a12b:free
   - Provider: nvidia
   - Base URL: https://integrate.api.nvidia.com/v1
   - Prompt: Ask for a thoughtful insight, explanation, or reasoning on a topic relevant to GenAI, technology, or a helpful explanation
2. **Extract the Response** from the subagent's output
3. **Post to Slack** using the send_message tool to the target channel

## Configuration
- Requires Slack integration to be set up
- Requires NVIDIA API key configured
- Target channel is configurable (defaults to general-reasoning)

## Troubleshooting (Direct Action - User Preferred)
Follow these steps in order - test after each step:

1. **Verify bot in channel & basic messaging**:
   - `/invite @hermes-bot` in target channel (e.g., #reasoning-nemotron-super-120b)
   - `hermes send_message -t slack:#channel -m "test"` 
   - If this fails, stop here - fix basic messaging first

2. **Check Slack configuration** (only if basic messaging works):
   - `hermes config get slack.require_mention` (should be false)
   - `hermes config get slack.free_response_channels` (should include your reasoning channel)
   - If wrong: `hermes config set slack.require_mention false` and/or `hermes config set slack.free_response_channels "general-nemotron-fast,genai-newsflash,genai-research,reasoning-nemotron-super-120b"`
   - Then: `hermes gateway restart`

3. **Verify cron job execution**:
   - `hermes cron list` (check last_run_at and last_status for reasoning-proactive job)
   - If not running: `hermes cron run <job_id>` to test manually

4. **Check delegation/NVIDIA setup**:
   - Verify NVIDIA_API_KEY is set in .env
   - Test a simple delegation: `hermes delegate_task --model nvidia/nemotron-3-super-120b-a12b:free --prompt "Say hello in kawaii style"` (should return quickly)
   - Review logs: `grep -i "slack-reasoning-proactive\|delegation\|120b" ~/.hermes/logs/gateway.log | tail -10`

**User Preference**: Each step includes immediate verification commands. Stop and fix at the first step that fails - don't proceed to theoretical explanations until basic functionality works.