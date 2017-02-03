#!/bin/sh

updatedb

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
		pip3 install $APP_DIST
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

		###
		### SETUP APPLICATION_SCRIP_NAME
		###
		if [ -z ${APPLICATION_SCRIP_NAME+x} ]
		then 
			echo "APPLICATION_SCRIP_NAME is not set - using default app.py"
			APPLICATION_SCRIP_NAME2=`locate app.py | head -1`
			echo "    using $APPLICATION_SCRIP_NAME2"
		else 
			APPLICATION_SCRIP_NAME2=`locate $APPLICATION_SCRIP_NAME | head -1`
			echo "APPLICATION_SCRIP_NAME is set - using $APPLICATION_SCRIP_NAME2"
		fi

		###
		### SETUP APPLICATION_CALLABLE_NAME
		###
		if [ -z ${APPLICATION_CALLABLE_NAME+x} ]
		then 
			echo "APPLICATION_CALLABLE_NAME is not set - using default app"
			APPLICATION_CALLABLE_NAME="app"
		else 
			echo "APPLICATION_CALLABLE_NAME is set - using $APPLICATION_CALLABLE_NAME"
		fi

		###
		### UWSGI_PROCESSES
		###
		if [ -z ${UWSGI_PROCESSES+x} ]
		then 
			echo "UWSGI_PROCESSES is not set - using default 4"
			UWSGI_PROCESSES=4
		else 
			echo "UWSGI_PROCESSES is set - using $UWSGI_PROCESSES"
		fi

		###
		### UWSGI_THREADS
		###
		if [ -z ${UWSGI_THREADS+x} ]
		then 
			echo "UWSGI_THREADS is not set - using default 2"
			UWSGI_THREADS=2
		else 
			echo "UWSGI_THREADS is set - using $UWSGI_THREADS"
		fi



		echo "Running uwsgi --ini $UWSGI_CONF in the backgroun"
		export R1=$(echo $APPLICATION_SCRIP_NAME2 | sed -e 's_/_\\/_g')
		sed -i -e "s/APPLICATIONSCRIPNAME/$R1/" $UWSGI_CONF
		sed -i -e "s/APPLICATIONCALLABLENAME/$APPLICATION_CALLABLE_NAME/g" $UWSGI_CONF
		sed -i -e "s/UWSGIPROCESSES/$UWSGI_PROCESSES/g" $UWSGI_CONF
		sed -i -e "s/UWSGITHREADS/$UWSGI_THREADS/g" $UWSGI_CONF
			
		uwsgi --ini $UWSGI_CONF &
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
	service nginx restart
else 
	echo "UWSGI_SITE_CONF is set to $UWSGI_SITE_CONF"
	if [ -e $UWSGI_SITE_CONF ]
	then
		echo "Setting up custom site and restarting nginx"
		rm -vf /etc/nginx/sites-enabled/*
		ln -s UWSGI_SITE_CONF /etc/nginx/sites-enabled/app.conf
		service nginx restart
	else
		echo "UWSGI_SITE_CONF file does not exist - falling back to default site"
		service nginx restart
	fi
fi

echo READY
while [ 1 ]; do
	sleep 60
done
