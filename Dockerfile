# TODO NOTES
# the boot script needs to start the guicorn process,
# and the rq worker process
# NOTE Miguel configures the image to either start in "guicorn" mode, or
# to start in "rq-worker" mode.  So the rq worker runs in a separate container
# from the guicorn process.

# - User Notes ----------------------------------------
#
# As per the README.md, the site-specific `.env` file must be bind-mounted into
# the container.

# - Developer Notes -----------------------------------
# 
# when this Dockerfile was written, the python modules
# py3-flask-sqlalchemy and py3-flask-migrate were available only in alpine edge
# testing for python version 3.10.  this may change in the future.
FROM python:3.10-alpine3.16
RUN apk -U upgrade
RUN apk add py3-mysqlclient py3-flask-sqlalchemy py3-flask-migrate --repository=http://dl-cdn.alpinelinux.org/alpine/edge/testing/
# pip will install to /usr/local, but apk will install the two above to /usr
ENV PYTHONPATH=/usr/lib/python3.10/site-packages:/usr/local/lib/python3.10/site-packages

# install the dependencies "early" so Docker build layers are cached
COPY requirements.txt /root/requirements.txt
RUN pip install --upgrade pip
RUN pip install -r /root/requirements.txt

# copy in the code and prepare to remove super-user status from the runtime
RUN adduser -h /app -s /bin/sh -D -u 22222 microblog
WORKDIR /app
COPY . .
RUN chown -R microblog /app

# run microblog
USER 22222
CMD ["/app/run.sh"]