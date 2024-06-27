#!/bin/bash

echo "Setting up crontab with schedule: $CRON_SCHEDULE"

IFS=',' read -r -a services <<< "$SERVICES"

echo "# Crontab for servarr-backup" > /etc/cron.d/servarr-backup

DELAY=0

for service in "${services[@]}"; do
  echo "Creating cron entry for service: $service"
  echo "$CRON_SCHEDULE root sleep $((DELAY * 60)) && /usr/local/bin/servarr backup create --type $service >> /var/log/servarr.log 2>&1" >> /etc/cron.d/servarr-backup
  DELAY=$((DELAY + 1))
done

chmod 0644 /etc/cron.d/servarr-backup

crontab /etc/cron.d/servarr-backup

echo "Selected services for backup: ${services[@]}"

touch /var/log/servarr.log

echo "Starting cron service..."
cron

tail -f /var/log/servarr.log
