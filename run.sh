#!/bin/sh
# Start the Microblog application server using gunicorn, after preparing the
# database and system-message translations.  Or, if MICROBLOG_RQ_WORKER_MODE
# is set to any value in the environment, start an RQ worker instead.

# https://unix.stackexchange.com/a/212189

if [ ! -f "/app/.env" ]; then
    echo "No /app/.env file detected, please check the README.md on what to do."
    exit
fi

if [ -n $MICROBLOG_RQ_WORKER_MODE ]; then
    echo "Preparing Microblog application server database and translations..."
    flask db upgrade
    flask translate compile

    # run the dummy mail server
    if [ -n $MICROBLOG_DUMMY_SMTP_SERVER ]; then
       echo "Starting dummy SMTP server, see Docker console output for emails."
       python -m smtpd -n -c DebuggingServer localhost:8025 &
    fi
       
    # send access and error to stdout so it is viewable within Docker
    echo "Starting Microblog application server through gunicorn..."
    exec gunicorn -b :5000 --access-logfile - --error-logfile - microblog:app
else
    echo "MICROBLOG_RQ_WORKER_MODE detected, starting rq worker..."
    rq worker microblog-tasks --url $REDIS_URL
fi
