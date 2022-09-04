FLASK_ENV="production"
FLASK_APP="microblog.py"
FLASK_RUN_HOST="0.0.0.0"
FLASK_RUN_PORT="5000"

# mail configuration -- must run local mail server for this to work
# `python -m smtpd -n -c DebuggingServer localhost:8025
MAIL_SERVER="localhost"
MAIL_PORT=8025
