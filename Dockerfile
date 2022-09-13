# - User Notes ----------------------------------------
#
# As per the README.md, the site-specific `.env` file must be bind-mounted into
# the container.

# - Developer Notes -----------------------------------
# 
# When this Dockerfile was written for alpine 3.16, the python modules
# py3-flask-sqlalchemy and py3-flask-migrate were available only in alpine edge
# testing for python version 3.10. 

# - Build Notes ---------------------------------------
#
# To build the image, `cd` into the directory containing this file, and:
#
# 1) `docker build -t ultasun/microblog .`

# - Run Notes -----------------------------------------
#
# To run, `cd` into the directory containing the `docker-compose.yml` file,
# and:
# 1) `docker compose up`

FROM python:3.10-alpine
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