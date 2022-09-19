# Miguel's Mega Flask Tutorial
See the tutorial on his blog [here](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world).  

**As of now, the maintainer of this repository had completed all 23 chapters of Miguel's Mega Flask tutorial.**  The homework in Chapter 23 has yet to be completed.

The goal of this repository is to provide notes for the maintainer of this repository, to learn [*Flask*](https://flask.palletsprojects.com/en/2.2.x/), and, to provide a demonstration of how Miguel's *Microblog* can be deployed as a *docker-compose.yml* orchestration (which considerably decreases the complexity of developing and deploying *Microblog*).

The strategy used here does not use [*venv*](https://docs.python.org/3/tutorial/venv.html) or any other *Python* virtualization environment system, **because *Docker* containerization is used instead.**  The maintainer of this repository had ran *Microblog* in *Docker* during the entire duration of studying the tutorial, since [*Chapter 1*](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world).  

This repository does not use *Heroku* to any extent, so the `Procfile` does not exist, nor does any content from [Chapter 18](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-xviii-deployment-on-heroku).

# Extensions from Miguel's work
This repository has a few extensions/modifications which are unique from Miguel's original tutorial:
1. The user-content translation feature uses *LibreTranslate* instead of the not-so-free *Microsoft* or *Google* translation API's
2. While Miguel did cover creating a *Docker* image of *Microblog*, he did not cover *orchestration* of a full-stack setup.  This repository will offer a `docker-compose.yml` file, and users will be able to `docker compose up` the entire system with one command.
3. The end of *Chapter 23* leaves implementing the remaining endpoints of the RESTful API as a reader exercise -- it will be done here.

# Installation with Docker
- See the main [`README.md`](https://github.com/ultasun/miguel_mega_flask/blob/master/README.md#installation), 
- The `docker-compose.yml` file may be [edited to enable bind-mounts](https://docs.docker.com/storage/bind-mounts/#use-a-bind-mount-with-compose) to map `/app` to a directory on the host system containing a clone of this repository.  
	- Ports for the individual services may also be exposed during development.

### Important Notes regarding *MySQL-python* *flask-sqlalchemy* & *flask-migrate* and *Alpine Linux*
There is a hand-writen `requirements.txt` file, however, three of the requirements had been commented out (`flask-sqlalchemy`, `flask-migrate`, and `MySQL-python`), and were instead installed from the *Alpine* *Testing*/*Community* repositories.  This was done in order to avoid installing an entire build environment (*GCC*) since the intention is to *Dockerize* Miguel's application after the final chapter of his tutorial.

# Installation without Docker
The following section will demonstrate how to start *Microblog* manually without the use of *Docker*.

**Please uncomment `MySQL-python`, `flask-sqlalchemy` and `flask-migrate` if the build environment is available to properly install these packages using `pip`.**  

Set up a [python virtual environment](https://docs.python.org/3/library/venv.html), and install the *Microblog* requirements:
      - Remove the comment (the `#` symbol) character from these three lines:
      	- `flask-sqlalchemy`
	- `flask-migrate`
	- `mysql-python`
      - `pip install -r requirements.txt`

Having credentials to an *SMTP* server will be necessary for real emails, but there is a built-in *SMTP* server which prints all sent emails to the terminal.

Setting up an *Elasticsearch* node will be necessary for proper site functionality, please read the *Elasticsearch* section below.

Setting up a *Redis* node and an *RQ* server to process work submitted by the application server will be necessary, see the *RQ* section and [Chapter 22](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-xxii-background-jobs) for more details.

A transient *SQLite3* database may be used, or, whichever *SQL* service supported by *SQLAlchemy* is available.  Be sure to install whichever libraries will be needed by [`flask-sqlalchemy`](https://flask-sqlalchemy.palletsprojects.com/en/2.x/) to connect to the provided *URI* string in `SQLALCHEMY_DATABASE_URI`.

After setting up all the support services, and after installing all the dependencies from `requirements.txt`, continue reading through the next section titled [*Starting the server manually*](#starting-the-server-manually).

## Starting the server manually without *Docker*.
Here is a list of commands to run in a terminal to manually start all processes which make up the full *Microblog* system functionality after performing a `git clone` into a [virtual environment](https://docs.python.org/3/library/venv.html):

1. Guarantee that all requirements packages are installed,
   - `pip install -r requirements.txt` does not fail as a process

2. Check `.flaskenv`
   - `FLASK_RUN_PORT` specifies which *TCP* port to run the *HTTP* server on.

3. Check `.env` in the top directory level of the repository
   - If it does not exist, then copy `.env.example` to `.env`,
   - Two Database options:
     1. Delete `SQLALCHEMY_DATABASE_URI` from the `.env` file to run *Microblog* with an in-memory, temporary *SQLite* database,
     2. or, set a [valid database URI](https://flask-sqlalchemy.palletsprojects.com/en/2.x/config/) with the value
       - For example,
       	 - `mysql://username:password@server/db`
	 - `sqlite:////tmp/test.db`
   - Three values in `.env` for *SMTP* settings, the default options are for the built-in server which prints emails to the terminal:
     1. `MAIL_SERVER=localhost`
     2. `MAIL_PORT=8025`
     3. `MICROBLOG_DUMMY_SMTP_SERVER=yes`
     	- If using a real *SMTP* server, delete this third line from the `.env.` file.
   - `SECRET_KEY` is used for [*CSRF*](https://en.wikipedia.org/wiki/Cross-site_request_forgery) protection.
     - Should make this randomly generated during the first boot.
   - `ADMINS` is a comma separated list of email addresses to send server logs.
   - `LANGUAGES` is a comma separated list of language codes enabled by [`flask translate`](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-xiii-i18n-and-l10n), a custom *cli* addition to automate *pybabel* tasks.
     - This value tells *Microblog* which languages are supposed to have been enabled by `flask translate compile`
     - `POSTS_PER_PAGE=33` dictates how many posts to display on each web page.
     - `LIBRETRANSLATE_MIRROR` can be [a public accessible mirror](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-xiii-i18n-and-l10n)
       - The default value from [`.env.example`](https://github.com/ultasun/miguel_mega_flask/blob/master/.env.example) is for when using [`docker-compose.yml`](https://github.com/ultasun/miguel_mega_flask/blob/master/docker-compose.yml)
     - Three options for *Elasticsearch*
       - `ELASTICSEARCH_URL_PREFIX`
       - `ELASTICSEARCH_HOST`
       - `ELASTICSEARCH_PORT`
     - `REDIS_URL` needs to include the database number:
       - `REDIS_URL=redis://redis:6379/0`, for example.
       
4. Start the simulated SMTP server,
   - Check `.env` that the following options are set:
     1. `MAIL_SERVER=localhost`
     2. `MAIL_PORT=8025`
     3. `MICROBLOG_DUMMY_SMTP_SERVER=yes`     
   - Run `python -u -m smtpd -n -c DebuggingServer localhost:8025`,
5. Start the *elasticsearch* server such that it does not require authentication,
   - Skipping this step will cause search queries in *Microblog* to fail,

6. Start the (*MySQL*) database server,
   - If using *postgresql* or other, be sure to adjust `requirements.txt`,

7. Start the *Redis* server such that it will have no authentication required,

8. Start an *rq* worker:
   - `rq worker microblog-tasks --url redis://localhost:6379/0`
9. Compile the system language translations and prepare the database:
   - `flask db upgrade`
   - `flask translate compile`
10. Optionally, run `flask shell` and do a pre-flight check:
   - No error messages after running `flask shell`,
   - Check if *LibreTranslate* is available:
   ```
   >>> from app.translate import translate as t
   >>> t('Hola todos.', 'es', 'en')
   ```
     - If using the [*LibreTranslate* docker image](), the result of running `t` will be a `Connection refused` if the *libretranslate* container is still initializing.
       - This is a process that takes between five and ten minutes.
     -  [More about running LibreTranslate](https://github.com/LibreTranslate/LibreTranslate#build-and-run) without *Docker*.
   - Check the database is accessible, try querying some [database models](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-iv-database),
   - Check that *redis* will be accessible:
   ```
   >>> from redis import Redis
   >>> redis_connection = Redis.from_url('redis://localhost:6379/0')
   ```
   - Check that *elasticsearch* will be accessible:
   ```
   >>> from elasticsearch import Elasticsearch
   >>> elasticsearch_connection = Elasticsearch('http://localhost:9200/')
   ```
   - Check that [*SMTP*](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-x-email-support) will be accessible
   
11. Start the server,
   - Run `flask run` in the terminal, follow the instructions on screen.

##### Production considerations
1. Start the server using *gunicorn*:
- `gunicorn -b localhost:3333 -w 3 microblog:app`
2. Read the section titled *Setting Up Nginx* [in Chapter 17](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-xvii-deployment-on-linux)
- Miguel shows an example `/etc/nginx/sites-enabled/` file
	- He deletes `/etc/nginx/sites-enabled/default`
	- He provides `/etc/nginx/sites-enabled/microblog`
- It appears Miguel uses *Nginx* as a proxy to support *HTTPS*.
- Another reason for using *Nginx* is to "*serve static files directly, and forward any requests intended for the application to the internal [gunicorn] server.*"
3. A way to automatically start and restart the *gunicorn* server during system reboots and crashes needs to be put in place, Miguel uses *Supervisor*.  See his Chapter 17 for more details.

# Components
The remainder of this document will explain *Microblog* components and features.

## Configuration
This is the order of files which should be checked by *the user* for setting various configuration options:
1. `.flaskenv` (check and set here **first**)
	- This file will override any values inherited from the shell environment.
		- If using *Docker*, best to use a bind-mount to overwrite this file.
2. Copy `.env.example` to `.env` and set this **second** 
	* Or set them in the shell environment, run `export` in your shell to verify the variables are set.)
		- If the values are set in `.env` then they will override what is inherited from the shell.
		- If using *Docker*, best to use a bind-mount to overwrite this file.
	- Ideally set sensitive values here (*SMTP* passwords, *API* keys, etc.)
3. `config.py` (check and set here **third**).
	- There should be no need to check or set this file, unless a finer grain of control is needed.

As a quick reminder, these four values are set in `.flaskenv`:
- `FLASK_RUN_HOST`
- `FLASK_RUN_PORT`
- `FLASK_ENV`
- `FLASK_APP`

## Models and Databases
[Chapter 4](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-iv-database) explains using the [*Migration*](https://flask-migrate.readthedocs.io/en/latest/) framework to manage the [*ORM*](https://en.wikipedia.org/wiki/Object–relational_mapping) system.

This way, adding new *models* to *Microblog* without losing old information is easy, and this is is done a few times in the tutorial.

## LibreTranslate
The system has the ability to detect which language the user submitted posts in, and to automatically translate them to a different user's local language based on their browser setting.

Miguel's tutorial shows using a translation service from either *Google* or *Microsoft* during [Chapter 14](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-xiv-ajax).  

A free alternative [*LibreTranslate*](https://libretranslate.com/) is available.  The [`app/translate.py`](https://github.com/ultasun/miguel_mega_flask/blob/master/app/translate.py) was [added on a separate commit](https://github.com/ultasun/miguel_mega_flask/commit/84f92299301743c7f827cdbd221a3e5f2c8a24ff) to help readers differentiate between Miguel's original work, and the effort shown here to utilize *LibreTranslate*.  See `app/translate.py` for this original effort.

The *LibreTranslate* mirror may need to be updated, since these are ran on an ad-hoc basis.  See the [mirror list](https://github.com/LibreTranslate/LibreTranslate#mirrors) and update the `LIBRETRANSLATE_MIRROR` value in `.env` to an appropriate value.  

In addition, if selecting to use the official mirror, an API key is required, and this key must be set under `LIBRETRANSLATE_API_KEY` in the `.env` file.

The `docker-compose.yml` file runs a *libretranslate* container, although it consumes considerable resources, so it may be more economical to use a [publicly available mirror](https://github.com/LibreTranslate/LibreTranslate#mirrors).

## Important Notes regarding *MySQL-python* *flask-sqlalchemy* & *flask-migrate* on *Alpine Linux*
The `requirements.txt` file will not install `flask-sqlaclhemy` and `flask-migrate`, because `pip` will attempt to use `gcc` to begin building things, which is undesirable when using *Alpine Linux* in a *Docker* container.  The point of using *Alpine Linux* in a *Docker* container is to minimize image size, and installing a build environment would thwart that goal.

*MySQL-python* also failed to install using `pip` inside the *alpine* container, but it is available from the system package manager using the *testing* repository.  

If using *Alpine Linux* in a *Docker* container, then at least `pip install flask-sqlalchemy` will fail, so enable the Alpine *testing* repository to install *Python* libraries which are not easily installed using `pip`:
1. Enable the `community` repository in /etc/apk/repositories, or, append `--repository=http://dl-cdn.alpinelinux.org/alpine/edge/testing/` to the next command:
2. `apk add py3-flask-migrate py3-flask-sqlalchemy py3-mysqlclient`
3.  Connect to the container with an updated `PYTHONPATH` environment variable:
- `docker exec -e PYTHONPATH="/usr/lib/python3.10/site-packages" -it <MyContainerNameOrId> /bin/sh`
	- Optionally consider to setup an additional virtualization layer with `venv`, etc., but this project is already a disposable container](https://github.com/ultasun/miguel_mega_flask/blob/master/Dockerfile#L33).
4.  Install the remaining *Microblog* requirements:
- `pip install -r requirements.txt`

Else, without using *Docker*, set up a [python virtual environment](https://docs.python.org/3/library/venv.html), and install the *Microblog* requirements:
      - Remove the comment (the `#` symbol) character from these three lines:
      	- `flask-sqlalchemy`
	- `flask-migrate`
	- `mysql-python`
      - `pip install -r requirements.txt`

## Logging via Emails
[Chapter 7](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-vii-error-handling) is about logging.  The microblog system developed in this series has the ability to email certain logs after certain error conditions occur.  

To use the built-in SMTP server for debugging purposes,
1. Automatic when using *Docker*
   - Set `MICROBLOG_DUMMY_SMTP_SERVER=yes` in `.env`.
     - **To disable**, delete (but do not comment) this line from the `.env` file.
     - Only [`run.sh`](https://github.com/ultasun/miguel_mega_flask/blob/master/run.sh#L25) uses this line.
2. Manual if needed prior to a manual invocation of `flask run`:
   - From a terminal, run:
     - `python -m smtpd -n -c DebuggingServer localhost:8025`,
   -  Set the following two environment variables in `.env` prior to `flask run`
	- `MAIL_SERVER=localhost`
	- `MAIL_PORT=8025`
	
Else, if using a real *SMTP* server,
      1. Set the following three values in `.env.`
      	- `MAIL_SERVER=example.mailserver.com`,
	- `MAIL_PORT=25`,
	- `MAIL_USE_TLS=yes`
	  - Delete this line from `.env` to disable TLS.

## I18n and L10n
Miguel's Microblog supports multiple languages.  The source code is written in *English*, and translations for *Spanish* have been prepared. 

Part of Miguel's tutorial is adding sub-commands to the `flask` command, they can be found in `app/cli.py`.

### Manual installation / debugging purposes (a fresh `git clone`)
After checking out this repository, and after installing all `pip` dependencies, a final step before launching the application server for the first time, is:

- `flask translate compile`

### Adding a new system language
This procedure is only necessary to have the system pages generate system messages in a language other than *English*.  That is, this has nothing to do with which languages users may compose their posts in. To add a new language:
1. `flask translate init <LANGUAGE-CODE>`
2. Get a translator, and update the new file with *poedit* or any text editor:
- `app/translations/<LANGUAGE-CODE>/LC_MESSAGES/messages.po`
3. `flask translate compile`
4. Update `.env` to include the new language code
- It is a comma separated list and must always include `en`. 

### Updating user-displayed statements
After adding or updating `_l()` or `_()` (user-displayed) statements, execute the following, or else, the (secondary language) text will not update when accessing the site:
1. `flask translate update`
2. Adjust each `messages.po` file for each language to include/update the translation(s) for each user-displayed statement.
3. `flask translate compile`
4. Check that `LANGUAGES` in `.env` is consistent with the languages available.
- It is a comma separated list and must always include `en`.

For troubleshooting, see [Chapter 13](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-xiii-i18n-and-l10n) of Miguel's tutorial.  The exact `pybabel` commands may be found in `app/cli.py`.

## Elasticsearch
[Chapter 16](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-xvi-full-text-search) is about [*Elasticsearch*](https://www.elastic.co).  

The easiest way to get an *Elasticsearch* instance running is to [start a *Docker* container](https://www.elastic.co/guide/en/elasticsearch/reference/current/run-elasticsearch-locally.html) using [the official *Elasticsearch* image](https://hub.docker.com/_/elasticsearch) with [**disabled security**](https://stackoverflow.com/a/47035057).  Disabling security on the *Elasticsearch* side is necessary, or else the examples shown by Miguel in his tutorial will not work line-for-line.

Run the following *Docker* command for an unsecured *Elasticsearch* instance:
`docker run -d -p 9200:9200 -e "discovery.type=single-node" -e "xpack.security.enabled=false" elasticsearch:8.4.0`

**Warning** From *Docker Hub*, the *Elasticsearch* image [must be *pulled* using an exact *version tag*](https://github.com/elastic/elasticsearch-docker/issues/215#issuecomment-439319831) such as `elasticsearch:8.4.0`. 

**Note** The above `docker run` command does not enable port-forwarding for port `9300` because this is a small development effort utilizing a single *Elasticsearch* node -- *Elasticsearch* serves users on port `9200`, and `9300` is used by multiple nodes to communicate with each other.

**Note** The `requirements.txt` file utilizes [an exact version](https://pypi.org/project/elasticsearch/8.4.0/) (`8.4.0`)), as does [the above `docker run` statement](https://hub.docker.com/layers/library/elasticsearch/8.4.0/images/sha256-f919f9d97aa008faad8669135357bd5de5c3f59cc42c410027f3b18c8adf0419) (`8.4.0`).

### Disabling Elasticsearch
For unit testing and development purposes, it may be appropriate to disable *Elasticsearch*.  In order to do this, disable one of the environment variables in the `.env` file.  If `config.py` detects that any of the three related environment variables are disabled (`None`) then *Microblog* will disable *Elasticsearch*.

## MySQL
[Chapter 17](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-xvii-deployment-on-linux) also covers how to use *MySQL* instead of *SQLite*, which is important because *SQLite* will lock the entire database during writes.  

After manually configuring *MySQL*, install the *models* for [`models.py`](https://github.com/ultasun/miguel_mega_flask/blob/master/app/models.py) using 
- `flask db upgrade`

## RQ
Chapter 22 is about using [*Redis*](https://redis.io) and [*RQ*](https://python-rq.org).

Using docker, the `rq` commands shown by Miguel will likely fail, because the *Redis* instance is likely running in a separate container from the *Python* environment.

Here is an example of using *RQ* from the command line with a specific server
`rq worker microblog-tasks --url redis://localhost:6379/0`

Starting `Queue` objects with a specific *URL* is self-explanatory following Miguel's tutorial:
`Redis.from_url('redis://192.168.1.13:6379/0')`

# Credits
Again, this is Miguel's Mega Flask Tutorial.  Some variation between [his original demonstrations](https://github.com/miguelgrinberg/microblog) and my following-along will be found -- in particular the exact usability of environment variables defined in `.env` (and `.env.example`). 

The `LICENSE` file included in this repository is an exact copy of the one [Miguel had distributed here](https://raw.githubusercontent.com/miguelgrinberg/microblog/v0.13/LICENSE).

The effort found in [`app/translate.py`](https://github.com/ultasun/miguel_mega_flask/blob/master/app/translate.py) is original, since Miguel did not cover how to utilize the *LibreTranslate* service.

The effort found in this `README.md` is also original and unique to this repository.  

Thank you for reading, and thank you Miguel for creating the [fine tutorial](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world). 
