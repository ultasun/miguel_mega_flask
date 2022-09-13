#!/bin/sh
# Start the Microblog application server using gunicorn, after preparing the
# database and system-message translations.  Or, if MICROBLOG_RQ_WORKER_MODE
# is set to any value in the environment, start an RQ worker instead.

# https://unix.stackexchange.com/a/212189

# sleep 11 seconds incase this is the first boot while other services prepare.
echo "Sleeping 30 seconds while other services become available..."
sleep 30
echo "...starting Microblog."

if [ ! -f "/app/.env" ]; then
    echo "No /app/.env file detected, please check the README.md on what to do."
    exit
else
    export $(cat "/app/.env" | xargs)
fi

if [ -z $MICROBLOG_RQ_WORKER_MODE ]; then
    echo "Preparing Microblog application server database and translations..."
    flask db upgrade &
    PID_FLASK_DB_UPGRADE=$!
    flask translate compile &

    # run the dummy mail server
    if [ -n $MICROBLOG_DUMMY_SMTP_SERVER ]; then
       echo "Starting dummy SMTP server, see Docker console output for emails."
       python -m smtpd -n -c DebuggingServer localhost:8025 &
    fi

    wait $PID_FLASK_DB_UPGRADE
    
    # send access and error to stdout so it is viewable within Docker
    echo "Starting Microblog application server through gunicorn..."
    exec gunicorn -b :5000 --access-logfile - --error-logfile - microblog:app
else
    echo "MICROBLOG_RQ_WORKER_MODE detected, starting rq worker..."
    rq worker microblog-tasks --url $REDIS_URL
fi
