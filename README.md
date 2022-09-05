# Miguel's Mega Flask Tutorial
See the tutorial on his blog [here](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world).  The goal of this repository is to provide notes for the maintainer of this repository, and, to provide Miguel's *Microblog* application as a *Docker* image (or at least, a working `Dockerfile`, available in this repository.)

As of now, the maintainer of this repository had completed at least *Chapter 12*.

# Installation
There is a `requirements.txt` file, however, two of the requirements had been commented out (`flask-sqlalchemy` and `flask-migrate`), and were instead installed from the *Alpine* *Testing* repository.  This was done in order to avoid installing an entire build environment (*GCC*) since the intention is to *Dockerize* Miguel's application after the final chapter of his tutorial.

**Please uncomment** `flask-sqlalchemy` and `flask-migrate` if the build environment is available to properly install these packages.  Else, read the section below titled *Important Notes (flask-sqlalchemy, flask-migrate)*, particularly for *Alpine Linux* in a *Docker* container.

# Configuration
This is the order of files which should be checked by *the user* for setting various configuration options:
1. `.flaskenv` (check and set here **first**)
2. `config.py` (check and set here **second**, because it uses values fed from `.flaskenv`)

The next two environment variables will likely need to be adjusted before running `flask run` in order to accept connections properly, especially if the application is running inside a *Docker* container:
* FLASK_RUN_HOST
* FLASK_RUN_PORT

# Important Notes (flask-sqlalchemy, flask-migrate)
The `requirements.txt` file will not install `flask-sqlaclhemy` and `
* On Alpine in a Docker container:
	* `pip install flask-sqlalchemy` will fail, so enable the Alpine *testing* repository to install:
		* `apk add py3-flask-migrate`
		* `apk add py3-flask-sqlalchemy`
	* Connect to the container with an updated `PYTHONPATH` environment variable:
		* `docker exec -e PYTHONPATH="/usr/lib/python3.10/site-packages" -it objective_stonebraker /bin/sh`

# Logging via Emails
Chapter 7 is about logging.  The microblog system developed in this series has the ability to email certain logs after certain error conditions occur. In order to set up the *dummy* mail server:

1. Run `python -m smtpd -n -c DebuggingServer localhost:8025` to start the *dummy server*
2. Set the following two environment variables:
	- `MAIL_SERVER=localhost`
	- `MAIL_PORT=8025`
	- `FLASK_ENV=production`

**Note** Placing these into `.flaskenv` seems wrong because the system has the ability to run without the email logging setup.  So the default behavior ought to be to not use the email logging.

# Emails as of Chapter 10
Chapter 10 of Miguel's tutorial adds more email functionality.  Here are some very important clarifications:

1. The `.flaskenv` file is where the environment variables should be declared, regarding exactly which mail (*SMTP*) server to connect to.
2. **Mail features will not work ***unless*** the `.flaskenv` variable** `FLASK_ENV=production` **is set!**
- That is, if `.flaskenv` has `FLASK_ENV=development`, then the mail features will not work, and there will be stack traces thrown by the server process when mail functions are attempted. 
3. The environment variable `MAIL_SERVER` must be set, too.

#### Note
 If the server is started in `FLASK_ENV=development` mode, then the `mail` variable is set to `None`, so stack traces thrown by the *python* process will reflect this...the reader will find `mail = None` (in `app/__init__.py` in the `else:` branch of `if not app.debug:`, and, again, in the `else:` branch of the inner conditional `if app.config['MAIL_SERVER']:`.  This decision was made because it increases readability of the stack traces thrown by the *python* process. 

The original code on Miguel's blog will result in a confusing `smtplib.SMTPServerDisconnected: please run connect() first` exception upon using any mail features after the server is started in `FLASK_ENV=development` mode (or without a `MAIL_SERVER`) -- the solution implemented in this repository (setting `mail = None`) will result in `NoneType` exceptions whenever mail features are attempted in `FLASK_ENV=development` mode.  

Hopefully, from a learning perspective, this increases system (and stack trace) clarity, since the `smtplib.SMTPServerDisconnected` exception could be thrown for reasons beyond the environment when the *python* process was started.  

# Language Support

Miguel's Microblog supports multiple languages.  The source code is written in *English*, and translations for *Spanish* have been prepared. 

Part of Miguel's tutorial is adding sub-commands to the `flask` command, 

### Adding a new language
To add a new language:
1. `flask translate init <LANGUAGE-CODE>`
2. Get a translator, and update the new file with *poedit* or any text editor:
- `app/translations/<LANGUAGE-CODE>/LC_MESSAGES/messages.po`
3. `flask translate compile`
4. `flask run` (this will start the server.)

### Updating user-displayed statements
After adding or updating `_l()` or `_()` (user-displayed) statements, execute the following, or else, the (secondary language) text will not update when accessing the site:
1. `flask translate update`
2. Adjust each `messages.po` file for each language to include/update the translation(s) for each user-displayed statement.
3. `flask translate compile`
4. `flask run` (this will start the server.)

For troubleshooting, see [Chapter 13](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-xiii-i18n-and-l10n) of Miguel's tutorial.

# Credits
Again, this is Miguel's Mega Flask Tutorial.  Some variation between his original demonstrations and my following-along will be found.  There is no `LICENSE` for this repository -- ask Miguel.


