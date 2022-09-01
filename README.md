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

# Credits
Again, this is Miguel's Mega Flask Tutorial.  Some variation between his original demonstrations and my following-along will be found.  There is no `LICENSE` for this repository -- ask Miguel.


