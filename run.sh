#!/bin/sh
# Start the Microblog application server using gunicorn, after preparing the
# database and system-message translations.  Or, if MICROBLOG_RQ_WORKER_MODE
# is set to any value in the environment, start an RQ worker instead.

# exit immediately if no /app/.env file is available.
if [ ! -f "/app/.env" ]; then
    echo "No /app/.env file detected, please check the README.md on what to do."
    exit
else
    # Read .env and set/export all found data as shell environment variables
    export $(cat "/app/.env" | xargs)
fi

# sleep 60 seconds incase this is the first boot while other services prepare.
if [ ! -f "/app/FIRST_BOOT" ]; then
    date > /app/FIRST_BOOT
    echo "Waiting 60 seconds for other services to complete first boot..."
    sleep 60
fi
echo "Starting Microblog..."

# run the dummy mail server, if enabled.
# note: both containers (worker & web) will have their own dummy server
if [ -n $MICROBLOG_DUMMY_SMTP_SERVER ]; then
    echo "Starting dummy SMTP server, see Docker console output for emails."

    # must redirect stderr to stdout (2>&1), then fork
    # must use unbuffered output (-u) to see messages in Docker console
    python -u -m smtpd -n -c DebuggingServer localhost:8025 2>&1 &
fi

# either start in RQ worker mode, or start in HTTP application server mode
if [ -z $MICROBLOG_RQ_WORKER_MODE ]; then
    echo "Preparing Microblog application server database and translations..."

    # doing two things at once (pages translations & db model preparations)
    flask db upgrade &
    PID_FLASK_DB_UPGRADE=$!
    flask translate compile
    wait $PID_FLASK_DB_UPGRADE
    
    # send access and error to stdout so it is viewable within Docker
    echo "Starting Microblog application server through gunicorn..."
    # overlay this PID with gunicorn using 'exec'
    exec gunicorn -b :5000 --access-logfile - --error-logfile - microblog:app
else
    echo "MICROBLOG_RQ_WORKER_MODE detected, starting rq worker..."
    
    rq worker microblog-tasks --url $REDIS_URL
fi
