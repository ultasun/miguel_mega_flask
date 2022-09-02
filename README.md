# Miguel's Mega Flask Tutorial
See the tutorial on his blog [here](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world).

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

# Credits
Again, this is Miguel's Mega Flask Tutorial.  Some variation between his original demonstrations and my following-along will be found.  There is no `LICENSE` for this repository -- ask Miguel.


