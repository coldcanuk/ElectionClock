# update_law_crontab.sh
#!/bin/bash

SCRIPT_DIR="/home/deployuser/web/ElectionClock"
LOG_FILE="/var/log/electionclock/maestro.log"

mkdir -p $(dirname "$LOG_FILE")

# Schedule maestro.py to run once a week
(crontab -l 2>/dev/null; echo "0 0 * * 1 cd $SCRIPT_DIR && /usr/bin/python3 maestro.py >> $LOG_FILE 2>&1") | crontab -
