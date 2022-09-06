# Miguel's Mega Flask Tutorial
See the tutorial on his blog [here](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world).  The goal of this repository is to provide notes for the maintainer of this repository, and, to provide Miguel's *Microblog* application as a *Docker* image (or at least, a working `Dockerfile`, available in this repository.)

As of now, the maintainer of this repository had completed at least *Chapter 16*.

The strategy used here does not use *venv* or any other *Python* virtualization environment system, because *Docker* containerization is used instead.  Setting up *venv* inside of a *Docker* container seems like fixing the same problem twice, and would otherwise complicate the setup needlessly.

Thanks to *Docker*, this document will not cover the traditional strategy of using *venv* or any other *Python* virtualization environment solution.

# Installation
There is a hand-writen `requirements.txt` file, however, two of the requirements had been commented out (`flask-sqlalchemy` and `flask-migrate`), and were instead installed from the *Alpine* *Testing* repository.  This was done in order to avoid installing an entire build environment (*GCC*) since the intention is to *Dockerize* Miguel's application after the final chapter of his tutorial.

**Please uncomment** `flask-sqlalchemy` and `flask-migrate` if the build environment is available to properly install these packages.  Else, read the section below titled [Important Notes regarding *flask-sqlalchemy* & *flask-migrate* on *Alpine Linux*](https://github.com/ultasun/miguel_mega_flask#important-notes-regarding-flask-sqlalchemy--flask-migrate-on-alpine-linux), particularly for when using *Alpine Linux* in a *Docker* container.

Please read the *Configuration* section regarding the mandatory `.env` file.  Failure to set the `.env` file may result in crashes and unexpected behavior.

Setting up an *Elasticsearch* node will be necessary for proper site functionality, please read the *Elasticsearch* section below.

Compiling all of the language translations for system messages and content will be necessary, and should be done as a final step before running the application server.

`flask translate compile`

Another final step is to instantiate the database tables.

`flask db upgrade`

Please read the next section titled *Configuration* before attempting to start the server.

# Configuration
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

As a quick reminder, these two values are set in `.flaskenv`:
- `FLASK_RUN_HOST`
- `FLASK_RUN_PORT`

The *LibreTranslate* mirror may need to be updated, since these are ran on an ad-hoc basis.  See the [mirror list](https://github.com/LibreTranslate/LibreTranslate#mirrors) and update the `LIBRETRANSLATE_MIRROR` value in `.flaskenv` to an appropriate value.  In addition, if selecting to use the official mirror, an API key is required, and this key must be set under `LIBRETRANSLATE_API_KEY`.

# Important Notes regarding *flask-sqlalchemy* & *flask-migrate* on *Alpine Linux*
The `requirements.txt` file will not install `flask-sqlaclhemy` and `flask-migrate`, because `pip` will attempt to use `gcc` to begin building things, which is undesirable when using *Alpine Linux* in a *Docker* container.  The point of using *Alpine Linux* in a *Docker* container is to minimize image size, and installing a build environment would thwart that goal.

If using *Alpine Linux* in a *Docker* container:
- `pip install flask-sqlalchemy` will fail, so enable the Alpine *testing* repository to install:
	- `apk add py3-flask-migrate`
	- `apk add py3-flask-sqlalchemy`
- Connect to the container with an updated `PYTHONPATH` environment variable:
	- `docker exec -e PYTHONPATH="/usr/lib/python3.10/site-packages" -it MyContainerNameOrId /bin/sh`
- Install the remaining *Microblog* requirements:
	- `pip install -r requirements.txt`

**Note** There seems to be no point in using *venv* or any other virtual environment system for *Python* because, this is already running in a *Docker* container.

# Logging via Emails
Chapter 7 is about logging.  The microblog system developed in this series has the ability to email certain logs after certain error conditions occur.  

Using a real *SMTP* server is a bit much for development and testing, so in order to set up the *dummy* mail server:

1. Run `python -m smtpd -n -c DebuggingServer localhost:8025` to start the *dummy server*,
2. Set the following two environment variables in `.env`
	- `MAIL_SERVER=localhost`
	- `MAIL_PORT=8025`

Else, if using a real *SMTP* server, then check `.env.example`.  **Warning** The system will enable *TLS* if any value is found in `MAIL_USE_TLS`, including words like *no*, *false*, etc.  If *TLS* is not desired, then comment out the line in `.env` and ensure no value for this variable would be inherited from the shell.

# Language Support
Miguel's Microblog supports multiple languages.  The source code is written in *English*, and translations for *Spanish* have been prepared. 

Part of Miguel's tutorial is adding sub-commands to the `flask` command, they can be found in `app/cli.py`.

### After Installation
After checking out this repository, and after installing all `pip` dependencies, a final step before launching the application server for the first time, is:

`flask translate compile`

### Adding a new system language
This procedure is only necessary to have the system pages generate system messages in a language other than *English*.  That is, this has nothing to do with which languages users may compose their posts in.

To add a new language:
1. `flask translate init <LANGUAGE-CODE>`
2. Get a translator, and update the new file with *poedit* or any text editor:
- `app/translations/<LANGUAGE-CODE>/LC_MESSAGES/messages.po`
3. `flask translate compile`
4. Update `.env` to include the new language code
- It is a comma separated list and must always include `en`. 
5. `flask run` (this will start the server.)

### Updating user-displayed statements
After adding or updating `_l()` or `_()` (user-displayed) statements, execute the following, or else, the (secondary language) text will not update when accessing the site:
1. `flask translate update`
2. Adjust each `messages.po` file for each language to include/update the translation(s) for each user-displayed statement.
3. `flask translate compile`
4. `flask run` (this will start the server.)

For troubleshooting, see [Chapter 13](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-xiii-i18n-and-l10n) of Miguel's tutorial.  The exact `pybabel` commands may be found in `app/cli.py`.

# Automatic translation of user content
The system has the ability to detect which language the user submitted posts in, and to automatically translate them to a different user's local language based on their browser setting.

Miguel's tutorial is a little dated (it's from 2017), and it has the reader use the translation service from either *Google* or *Microsoft* during [Chapter 14](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-xiv-ajax).  

A free alternative [*LibreTranslate*](https://libretranslate.com/) is available.  The [`app/translate.py`](https://github.com/ultasun/miguel_mega_flask/blob/master/app/translate.py) was [added on a separate commit](https://github.com/ultasun/miguel_mega_flask/commit/84f92299301743c7f827cdbd221a3e5f2c8a24ff) to help readers differentiate between Miguel's original work, and the effort shown here to utilize *LibreTranslate*.  See `app/translate.py` for this original effort.

# Elasticsearch
[Chapter 16](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-xvi-full-text-search) is about [*Elasticsearch*](https://www.elastic.co).  

The easiest way to get an *Elasticsearch* instance running is to [start a second *Docker* container](https://www.elastic.co/guide/en/elasticsearch/reference/current/run-elasticsearch-locally.html) using [the official *Elasticsearch* image](https://hub.docker.com/_/elasticsearch) with [**disabled security**](https://stackoverflow.com/a/47035057).  Disabling security on the *Elasticsearch* side is necessary, or else the examples shown by Miguel in his tutorial will not work line-for-line.

Run the following *Docker* command for an unsecured *Elasticsearch* instance:
`docker run -d -p 9200:9200 -e "discovery.type=single-node" -e "xpack.security.enabled=false" elasticsearch:8.4.0`

**Warning** From *Docker Hub*, the *Elasticsearch* image [must be *pulled* using an exact *version tag*](https://github.com/elastic/elasticsearch-docker/issues/215#issuecomment-439319831) such as `elasticsearch:8.4.0`. 

**Note** The above `docker run` command does not enable port-forwarding for port `9300` because this is a small development effort utilizing a single *Elasticsearch* node -- *Elasticsearch* serves users on port `9200`, and `9300` is used by multiple nodes to communicate with each other.

**Note** The `requirements.txt` file utilizes [an exact version](https://pypi.org/project/elasticsearch/8.4.0/) (`8.4.0`)), as does [the above `docker run` statement](https://hub.docker.com/layers/library/elasticsearch/8.4.0/images/sha256-f919f9d97aa008faad8669135357bd5de5c3f59cc42c410027f3b18c8adf0419) (`8.4.0`).

### Disabling Elasticsearch
For unit testing and development purposes, it may be appropriate to disable *Elasticsearch*.  In order to do this, disable one of the environment variables in the `.env` file.  If `config.py` detects that any of the three related environment variables are disabled (`None`) then *Microblog* will disable *Elasticsearch*.

# Starting the server 
There are two ways to start the server.

### Development mode
Start the server with:
`flask run`

### Production mode
1. Start the server using *gunicorn*:
- `gunicorn -b localhost:3333 -w 3 microblog:app`
2. Read the section titled *Setting Up Nginx* [in Chapter 17](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-xvii-deployment-on-linux)
- Miguel shows an example `/etc/nginx/sites-enabled/` file
	- He deletes `/etc/nginx/sites-enabled/default`
	- He provides `/etc/nginx/sites-enabled/microblog`
- It appears Miguel uses *Nginx* as a proxy to support *HTTPS*.
- Another reason for using *Nginx* is to "*serve static files directly, and forward any requests intended for the application to the internal [gunicorn] server.*"
3. A way to automatically start and restart the *gunicorn* server during system reboots and crashes needs to be put in place, Miguel uses *Supervisor*.  See his Chapter 17 for more details.

#### MySQL
Chapter 17 also covers how to use *MySQL* instead of *SQLite*, which is important because *SQLite* will lock the entire database during writes.  

*MySQL* requires a database to be made, 
`CREATE DATABASE microblog CHARACTER SET utf8 COLLATE utf8_bin;`
along with a user,
`CREATE USER 'microblog'@'localhost' IDENTIFIED BY 'some-password';
and their privileges to be set,
`GRANT ALL PRIVILEGES ON microblog.\* TO 'microblog'@'localhost';`
and flushed
`FLUSH PRIVILEGES;`
Then, `flask db upgrade` will be able to create the tables.

# Credits
Again, this is Miguel's Mega Flask Tutorial.  Some variation between [his original demonstrations](https://github.com/miguelgrinberg/microblog) and my following-along will be found -- in particular the exact usability of environment variables defined in `.env` (and `.env.example`). 

The `LICENSE` file included in this repository is an exact copy of the one [Miguel had distributed here](https://raw.githubusercontent.com/miguelgrinberg/microblog/v0.13/LICENSE).

The effort found in [`app/translate.py`](https://github.com/ultasun/miguel_mega_flask/blob/master/app/translate.py) is original, since Miguel did not cover how to utilize the *LibreTranslate* service.

The effort found in this `README.md` is also original and unique to this repository.  

Thank you for reading, and thank you Miguel for creating the [fine tutorial](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world). 


