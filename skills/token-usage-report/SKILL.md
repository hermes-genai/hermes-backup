---
name: token-usage-report
description: "Report token usage for today via Hermes insights"
version: 1.0.0
author: Hermes Agent
platforms: [linux]
prerequisites:
  commands: [hermes]
metadata:
  hermes:
    tags: [token, usage, insights, reporting]
---

# Token Usage Report Skill

This skill runs `hermes insights --days 1` to get token usage for the past day and formats it for Slack delivery.

## Usage

When run, this skill will:
1. Execute `hermes insights --days 1` to get token usage statistics
2. Format the output into a readable message
3. Return the message for delivery to Slack (or other platforms)

## Output Format

The skill returns a plain text message suitable for Slack, containing:
- Total token usage for today
- Breakdown by model/provider if available
- Any other relevant insights from the Hermes insights command

## Example Output

```
📊 Hermes Token Usage Report (Today)
───────────────────────────────────
Total tokens: 125,430
- nvidia/nemotron-3-super-120b: 85,210 tokens
- nvidia/nemotron-3-nano: 40,220 tokens

Tools used: web_search (45), terminal (30), file_read (25)
```

---
# Skill Implementation

The skill works by executing the `hermes insights` command and capturing its output.