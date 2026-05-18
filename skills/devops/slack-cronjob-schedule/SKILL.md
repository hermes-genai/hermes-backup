---
name: slack-cronjob-schedule
category: devops
description: Ensure Hermes cron jobs delivering to Slack run only during acceptable hours (07:00–20:00 Berlin time).
---
Purpose: Ensure that any Hermes cron job that delivers messages to Slack channels only runs during acceptable hours (e.g., 07:00–20:00 local Berlin time) to avoid nighttime disturbances.

## When to Use
- Creating a new cron job that posts to a Slack channel.
- Updating an existing Slack‑directed cron job’s schedule.
- Reviewing existing Slack jobs for compliance with quiet‑hours policy.

## Steps

1. **Determine local Berlin time window**  
   - Acceptable window: **07:00 – 20:00** (inclusive).  
   - Convert to UTC for cron: subtract 2 hours (CEST) → **05:00 – 18:00 UTC**.  
   - If Berlin is on CET (UTC+1), adjust accordingly (06:00–19:00 UTC).  
   - For simplicity, use CEST offset (most of year).

2. **Construct a cron expression**  
   - Use fields: `minute hour day month weekday`.  
   - To restrict to the window, set `hour` range: `5-18` (UTC).  
   - Example for hourly at minute 0: `0 5-18 * * *`.  
   - Example for every 30 minutes: `0,30 5-18 * * *`.  
   - Example for specific times (e.g., 08:00 and 16:00 Berlin): `0 6,14 * * *` (UTC).

3. **Create or update the cron job**  
   - Use Hermes CLI or `cronjob` tool:  
     ```bash
     hermes cronjob create --name "my-slack-job" \
         --schedule "0 5-18 * * *" \
         --deliver "slack:#my-channel" \
         --prompt "Your prompt here"
     ```
   - To update an existing job:  
     ```bash
     hermes cronjob update <job_id> --schedule "0 5-18 * * *"
     ```

4. **Verify the schedule**  
   - List the job and inspect `next_run_at` and `schedule`:  
     ```bash
     hermes cronjob list
     ```
   - Ensure the next run falls within the allowed window.  
   - Optionally, run a dry‑run with `hermes cronjob run <job_id>` to see immediate delivery.

5. **Document the quiet‑hours rule**  
   - Add a comment in the job’s description or in a project README:  
     `# Slack delivery restricted to 07:00–20:00 Berlin time`.

## Pitfalls & How to Avoid Them
- **Assuming UTC equals local time** → Always convert Berlin time to UTC before writing the cron expression.  
- **Forgetting daylight‑shifts** → If you need exact wall‑clock times year‑round, consider two schedules (one for CEST, one for CET) or use a wrapper script that checks local time. For most use‑cases, using CEST (UTC+2) is acceptable as the drift is only one hour in winter.  
- **Over‑restricting** → If a job must run outside the window (e.g., critical alerts), explicitly document the exception and consider delivering to a different channel (e.g., Telegram) or using a separate emergency mechanism.  
- **Mis‑typing ranges** → Remember cron hour field is 0‑23; `5-18` includes 5,6,…,18. Double‑check with a cron expression tester if unsure.

## Verification Checklist
- [ ] Job delivers to a Slack channel.  
- [ ] Cron schedule hour range matches `5-18` (UTC) for Berlin CEST.  
- [ ] Next run time (from `cronjob list`) is between 07:00 and 20:00 Berlin.  
- [ ] No Slack deliveries observed outside the window during a 24‑hour test period.  
- [ ] Documentation updated with the quiet‑hours rule.

## Related Tools
- `cronjob` tool (create, update, list, run).  
- `send_message` tool (for testing delivery).  
- `skill_view` for referencing other skills (e.g., `slack-proactive-engagement`).

## Reference Files
- See `references/cron_examples.md` for ready-to-use cron expression examples converted to Berlin time.

## Example
Creating a daily reflection job at 18:00 Berlin (16:00 UTC):
```bash
hermes cronjob create \
  --name "ada-daily-reflection" \
  --schedule "0 16 * * *" \
  --deliver "slack:#ada-daily-reflection" \
  --prompt "Write a short daily development diary for the Slack channel #ada-daily-reflection in English..."
```

---
*This skill encapsulates the user’s preference to keep Slack interactions limited to daytime hours, ensuring a respectful and non‑intrusive Hermes presence.*