# Miguel Grinberg Mega Flask Tutorial

*Miguel Grinberg* had [wrote an excellent tutorial series](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world) on developing a full stack web application system using the [*Flask*](https://flask.palletsprojects.com/en/2.2.x/) framework.

His system has the reader utilize much more, including [*Elasticsearch*](https://www.elastic.co/), [*Redis*](https://redis.io), [*RQ*](https://python-rq.org) and [*SQLAlchemy*](https://flask-sqlalchemy.palletsprojects.com).

The system is called *Microblog*.

The [maintainer of this repository](https://github.com/ultasun) had expanded on Miguel's excellent work:
1. [This *Microblog*](https://github.com/ultasun/miguel_mega_flask/blob/master/app/translate.py) will use [*LibreTranslate*](https://github.com/LibreTranslate/LibreTranslate) to provide translation services to users.
   - This *Microblog* has all translation queries served internally.
   - Miguel's original tutorial has the reader [use an external translation API](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-xiv-ajax/page/4)
2. This *Microblog* provides a stand-alone [`docker-compose.yml`](https://github.com/ultasun/miguel_mega_flask/blob/master/docker-compose.yml), which allows for easy deployment of the full stack system.
   - The only other file needed by users to bring up *Microblog* is a [configuration file](https://github.com/ultasun/miguel_mega_flask/blob/master/.env.example).

# Installation
1. Install [*Docker*](https://www.docker.com/), [*Docker Desktop*](https://www.docker.com/products/docker-desktop/) or [*Podman*](https://podman.io),
2. Download [`docker-compose.yml`](https://github.com/ultasun/miguel_mega_flask/blob/master/docker-compose.yml),
3. Download [`.env.example`](https://github.com/ultasun/miguel_mega_flask/blob/master/.env.example),
   - Rename it to `.env`, and then,
   - Place it into the same directory as `docker-compose.yml`,
4. Using a terminal, `cd` to the directory containing both `docker-compose.yml` and `.env`, and run:
   - `docker compose up`
5. **Wait about 15 minutes** (or longer) for:
   - All images to download (the *LibreTranslate* image is large),
   - After the *LibreTranslate* container starts, it takes about 10 more minutes before it will begin serving translation requests,
6. Using a web browser, access the service on standard *HTTP* port `80`!
   - For example, [http://localhost/](http://localhost/)

# More information
There is an [original `README.old.md`](https://github.com/ultasun/miguel_mega_flask/blob/master/README.old.md) which was used by the maintainer of this repository while following Miguel's tutorial.  That `README.old.md` has notes which, ultimately, have been translated into the [`run.sh`](https://github.com/ultasun/miguel_mega_flask/blob/master/run.sh), `Dockerfile`, `docker-compose.yml`, and more.

# Credits
The original tutorial was written by [*Miguel Grinberg*](https://blog.miguelgrinberg.com).  All the code in this repository was physically typed on a keyboard by [*ultasun*](https://github.com/ultasun) while following *Miguel's* tutorial.

Thanks Miguel!  Thank you for reading.
