# Miguel's Mega Flask Tutorial
See the tutorial on his blog [here](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world).

# Configuration
This is the order of files which should be checked by *the user* for setting various configuration options:
1. `.flaskenv` (check and set here **first**)
2. `config.py` (check and set here **second**, because it uses values fed from `.flaskenv`)

# Notes:
* Useful environment variables for `flask run`
	* FLASK_RUN_HOST
	* FLASK_RUN_PORT
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

# Credits
Again, this is Miguel's Mega Flask Tutorial.  Some variation between his original demonstrations and my following-along will be found.  There is no `LICENSE` for this repository -- ask Miguel.


