# Cron Expression Examples for Slack Jobs (Berlin Time)

All times assume Berlin CEST (UTC+2). Adjust for CET (UTC+1) by adding 1 hour to UTC times.

## Hourly at minute 0
- Schedule: `0 5-18 * * *`
- Runs at: 07:00, 08:00, ..., 20:00 Berlin

## Every 30 minutes
- Schedule: `0,30 5-18 * * *`
- Runs at: 07:00, 07:30, 08:00, 08:30, ..., 20:00, 20:30 Berlin

## Twice daily (08:00 and 16:00 Berlin)
- Schedule: `0 6,14 * * *`
- Runs at: 08:00 and 16:00 Berlin

## Daily at 18:00 Berlin
- Schedule: `0 16 * * *`
- Runs at: 18:00 Berlin

## Daily at 07:00 Berlin
- Schedule: `0 5 * * *`
- Runs at: 07:00 Berlin

## Note on daylight saving
- The above uses CEST offset (UTC+2). In winter (CET, UTC+1), add 1 hour to the Berlin times.
- For year-round exact wall-clock times, consider using two schedules or a wrapper script.