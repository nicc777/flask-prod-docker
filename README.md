# Flask Production Docker Container

Just started with the project - will update the README in a couple of days

# Building 

Using docker:

	$ docker build --no-cache -t flask-prod-docker:latest .

# Environment variables

* `DEBUG` Setting that will be passed to `FLASK_DEBUG` in the `start.sh` script `default=0`
* `SYSLOG_SERVER` might be useful for your flask application, otherwise unused `default=127.0.0.1`
* `SYSLOG_PORT` works with `SYSLOG_SERVER` `default=541`
* `SYSLOG_LEVEL` works with `SYSLOG_SERVER` `default=ERROR`
* `AWS_DEFAULT_REGION` available to your app `optional` `default=us-east-1`
* `AWS_ACCESS_KEY_ID` available to your app `optional` `default=not-set`
* `AWS_SECRET_ACCESS_KEY` available to your app `optional` `default=not-set`
* `APP_DIST` The flask application package to install `default=/opt/dist/app.tar.gz`
* `UWSGI_CONF` location of your uwsgi ini file `default=/opt/conf/app.ini`
* `UWSGI_SITE_CONF` location of the nginx based configuration for the uwsgi site `default=/opt/conf/app.conf`
* `APPLICATION_SCRIP_NAME` will be used to set `FLASK_APP` in `start.sh` and used to set the application in the uwsgi ini file `default=app.py`
* `APPLICATION_CALLABLE_NAME` the name of the callable application. in most cases `app` or `application` will work `default=app`


# Using the example

NOTE: Still busy working on the example...

You can run the following for a quick test (assuming you have cloned the repository)

	$ cd example
	$ python3 setup.py sdist
	$ docker run -ti --rm \
	-e "APPLICATION_SCRIP_NAME=app1.py" \
	-p 127.0.0.1:8080:8080 \
	flask-prod-docker

