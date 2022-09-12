# TODO NOTES
# the boot script needs to start the guicorn process,
# and the rq worker process
# NOTE Miguel configures the image to either start in "guicorn" mode, or
# to start in "rq-worker" mode.  So the rq worker runs in a separate container
# from the guicorn process.

# ------------------------------------
# when this Dockerfile was written, the python modules
# py3-flask-sqlalchemy and py3-flask-migrate were available only in alpine edge
# testing for python version 3.10.  this may change in the future.
FROM python:3.10-alpine3.16
RUN apk -U upgrade
RUN apk add py3-flask-sqlalchemy py3-flask-migrate --repository=http://dl-cdn.alpinelinux.org/alpine/edge/testing/
ENV PYTHONPATH=/usr/lib/python3.10/site-packages

RUN pip install --upgrade pip
RUN adduser -h /app -s /bin/sh -D -u 22222 microblog
WORKDIR /app
COPY . .
RUN chown -R microblog /app

USER 22222
RUN pip install -r requirements.txt
CMD ["sh"]