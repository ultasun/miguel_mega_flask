#!/bin/sh
# Start the Microblog application server using gunicorn, after preparing the
# database and system-message translations.  Or, if MICROBLOG_RQ_WORKER_MODE
# is set to any value in the environment, start an RQ worker instead.

# https://unix.stackexchange.com/a/212189

if [ ! -f "/app/.env" ]; then
    echo "No /app/.env file detected, please check the README.md on what to do."
    exit
fi

if [ -z ${MICROBLOG_RQ_WORKER_MODE+x} ]; then
    echo "Preparing Microblog application server database and translations..."
    flask db upgrade
    flask translate compile
    # send access and error to stdout so it is viewable within Docker
    echo "Starting Microblog application server through gunicorn..."
    exec gunicorn -b :5000 --access-logfile - --error-logfile - microblog:app
else
    echo "MICROBLOG_RQ_WORKER_MODE detected, starting rq worker..."
    rq worker microblog-tasks --url $REDIS_URL
fi
