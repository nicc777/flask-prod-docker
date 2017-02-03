# Flask Production Docker Container

## What is this...

I experiment a lot so I needed an easy way to get [Flask](http://flask.pocoo.org/) applications ready for more production like environments, using [nginx](https://www.nginx.com/) to reverse proxy requests to the flask application hosted via [uwsgi](https://uwsgi-docs.readthedocs.io/en/latest/).

Therefore, the docker container will serve the following:

	nginx (port 80) --> uwsgi (port 8080) --> your flask application

## AWS

I use AWS a lot so my example is AWS ready in that you can set the required keys.

The AWS command line utilities as well as [boto3](https://boto3.readthedocs.io/en/latest/) is also installed.

# Building

Using docker:

	$ docker build --no-cache -t flask-prod-docker:latest .

# Quick start

Use the following example to quickly run the example:

	$ cd /tmp
	$ git clone https://github.com/nicc777/flask-prod-docker.git
    $ cd flask-prod-docker/example/
	$ python3 setup.py sdist
    $ mkdir -p ../test/conf
    $ cp -vf conf/* ../test/conf/
	$ cd ../test
	$ docker run -ti --rm                           \
	-v "$PWD/conf:/opt/conf"                        \
	-v "$PWD/../example/dist/:/opt/dist"            \
	-e "APPLICATION_SCRIP_NAME=app1.py"             \
	-e "APPLICATION_CALLABLE_NAME=app"              \
	-e "UWSGI_CONF=/opt/conf/uwsgi.ini"             \
	-e "UWSGI_SITE_CONF=/opt/conf/app.conf"         \
	-e "APP_DIST=/opt/dist/flask-app-0.0.1.tar.gz"  \
	-p 127.0.0.1:8080:80                            \
	flask-prod-docker

Finally, in another terminal:

	$ curl http://127.0.0.1:8080/
	Hello, World!

In your docker container terminal you should see:

	Installing /opt/dist/flask-app-0.0.1.tar.gz
	   .
	   .
	   .
	*** Stats server enabled on 127.0.0.1:9191 fd: 15 ***
	                                                                                                                        [ OK ]
	READY
	[pid: 65|app: 0|req: 1/1] 172.17.0.1 () {32 vars in 340 bytes} [Fri Feb  3 03:49:45 2017] GET / => generated 13 bytes in 11 msecs (HTTP/1.1 200) 2 headers in 79 bytes (1 switches on core 0)

You can now create your own flask application!

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
* `UWSGI_PROCESSES` number of uwsgi processes `default=4`
* `UWSGI_THREADS` number of uwsgi threads `default=2`
* `APPLICATION_SCRIP_NAME` will be used to set `FLASK_APP` in `start.sh` and used to set the application in the uwsgi ini file `default=app.py`
* `APPLICATION_CALLABLE_NAME` the name of the callable application. in most cases `app` or `application` will work `default=app`


# Configuration files

## Example uwsgi ini file

Also see `example/conf/uwsgi.ini`:

	[uwsgi]
	socket = 127.0.0.1:8080
	wsgi-file = APPLICATIONSCRIPNAME
	callable = APPLICATIONCALLABLENAME
	processes = UWSGIPROCESSES
	threads = UWSGITHREADS
	stats = 127.0.0.1:9191

The above example is considered the minimum you should have in your config. Note that the following text will be replaced by the start script:

* APPLICATIONSCRIPNAME
* APPLICATIONCALLABLENAME
* UWSGIPROCESSES
* UWSGITHREADS

## Example nginx conf file

Also see `example/conf/app.conf`:

	server {
	  location / {
	    include uwsgi_params;
	    uwsgi_pass 127.0.0.1:8080;
	  }
	}

You should not need more than the above, but feel free to add more as needed.