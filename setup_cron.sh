#!/bin/bash
# Setup daily cron job for JobServe applications

# Add cron job to run daily at 9 AM
(crontab -l 2>/dev/null; echo "0 9 * * * cd $(pwd) && python3 daily_job_scheduler.py") | crontab -

echo "Cron job added: Daily run at 9 AM"
echo "Current crontab:"
crontab -l

