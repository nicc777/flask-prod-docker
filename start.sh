#!/bin/sh

#######################################
#
# INSTALL APP
#
#######################################

if [ -z ${APP_DIST+x} ]
then 
	echo "APP_DIST is not set - not installing app" 
else 
	echo "APP_DIST is set to $APP_DIST - attempting to install using pip3"
	if [ -e $APP_DIST ]
	then
		echo "Installing $APP_DIST"
		# pip3 install $APP_DIST
	else
		echo "Installation file does not exist - SKIPPING"
	fi
fi

#######################################
#
# PREP UWSGI
#
#######################################

if [ -z ${UWSGI_CONF+x} ]
then 
	echo "UWSGI_CONF is not set - not starting UWSGI" 
else 
	echo "UWSGI_CONF is set to $UWSGI_CONF"
	if [ -e $UWSGI_CONF ]
	then
		echo "Running uwsgi --ini $UWSGI_CONF in the backgroun"
		# sed /APPLICATION_SCRIP_NAME/$APPLICATION_SCRIP_NAME/g $UWSGI_CONF
		# sed /APPLICATION_CALLABLE_NAME/$APPLICATION_CALLABLE_NAME/g $UWSGI_CONF
		# uwsgi --ini $UWSGI_CONF &
	else
		echo "UWSGI file does not exist - SKIPPING"
	fi
fi

#######################################
#
# PREP NGINX
#
#######################################

if [ -z ${UWSGI_SITE_CONF+x} ]
then 
	echo "UWSGI_SITE_CONF is not set - using default nginx site" 
else 
	echo "UWSGI_SITE_CONF is set to $UWSGI_SITE_CONF"
	if [ -e $UWSGI_SITE_CONF ]
	then
		echo "Setting up custom site and restarting nginx"
		# rm -vf /etc/nginx/sites-enabled/*
		# ln -s UWSGI_SITE_CONF /etc/nginx/sites-enabled/app.conf
		# service nginx restart
	else
		echo "UWSGI_SITE_CONF file does not exist - falling back to default site"
	fi
fi

echo READY
while [ 1 ]; do
	sleep 60
done
