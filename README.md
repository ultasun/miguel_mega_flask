# Miguel's Mega Flask Tutorial
See the tutorial on his blog [here](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world).  The goal of this repository is to provide notes for the maintainer of this repository, and, to provide Miguel's *Microblog* application as a *Docker* image (or at least, a working `Dockerfile`, available in this repository.)

As of now, the maintainer of this repository had completed at least *Chapter 13*.

# Installation
There is a hand-writen `requirements.txt` file, however, two of the requirements had been commented out (`flask-sqlalchemy` and `flask-migrate`), and were instead installed from the *Alpine* *Testing* repository.  This was done in order to avoid installing an entire build environment (*GCC*) since the intention is to *Dockerize* Miguel's application after the final chapter of his tutorial.

**Please uncomment** `flask-sqlalchemy` and `flask-migrate` if the build environment is available to properly install these packages.  Else, read the section below titled *Important Notes (flask-sqlalchemy, flask-migrate)*, particularly for *Alpine Linux* in a *Docker* container.

Please read the *Configuration* section regarding the mandatory `.env` file.  Failure to set the `.env` file may result in crashes and unexpected behavior.

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
- FLASK_RUN_HOST
- FLASK_RUN_PORT

The *LibreTranslate* mirror may need to be updated, since these are ran on an ad-hoc basis.  See the [mirror list](https://github.com/LibreTranslate/LibreTranslate#mirrors) and update the `LIBRETRANSLATE_MIRROR` value in `.flaskenv` to an appropriate value.  In addition, if selecting to use the official mirror, an API key is required, and this key must be set under `LIBRETRANSLATE_API_KEY`.

# Important Notes (flask-sqlalchemy, flask-migrate)
The `requirements.txt` file will not install `flask-sqlaclhemy` and `flask-migrate`
- On Alpine in a Docker container:
	- `pip install flask-sqlalchemy` will fail, so enable the Alpine *testing* repository to install:
		- `apk add py3-flask-migrate`
		- `apk add py3-flask-sqlalchemy`
	- Connect to the container with an updated `PYTHONPATH` environment variable:
		- `docker exec -e PYTHONPATH="/usr/lib/python3.10/site-packages" -it MyContainerNameOrId /bin/sh`

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

Part of Miguel's tutorial is adding sub-commands to the `flask` command, 

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

For troubleshooting, see [Chapter 13](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-xiii-i18n-and-l10n) of Miguel's tutorial.

# Automatic translation of user content
The system has the ability to detect which language the user submitted posts in, and to automatically translate them to a different user's local language based on their browser setting.

Miguel's tutorial is a little dated (it's from 2017), and it has the reader use the translation service from either *Google* or *Microsoft* during [Chapter 14](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-xiv-ajax).  

A free alternative [*LibreTranslate*](https://libretranslate.com/) is available.  The [`app/translate.py`](https://github.com/ultasun/miguel_mega_flask/blob/master/app/translate.py) was [added on a separate commit](https://github.com/ultasun/miguel_mega_flask/commit/84f92299301743c7f827cdbd221a3e5f2c8a24ff) to help readers differentiate between Miguel's original work, and the effort shown here to utilize *LibreTranslate*.  See `app/translate.py` for this original effort.

# Credits
Again, this is Miguel's Mega Flask Tutorial.  Some variation between [his original demonstrations](https://github.com/miguelgrinberg/microblog) and my following-along will be found.  The `LICENSE` file included in this repository is an exact copy of the one [Miguel had distributed here](https://raw.githubusercontent.com/miguelgrinberg/microblog/v0.13/LICENSE).

The effort found in [`app/translate.py`](https://github.com/ultasun/miguel_mega_flask/blob/master/app/translate.py) is original, since Miguel did not cover how to utilize the *LibreTranslate* service.

Thank you for reading, and thank you Miguel for creating the [fine tutorial](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world). 


