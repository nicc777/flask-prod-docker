FROM ubuntu:latest
MAINTAINER Nico Coetzee <nicc777@gmail.com>

LABEL Description="A container for the production hosting of a flask application" Vendor="none" Version="0.1"

RUN apt-get update && apt-get upgrade -y
RUN apt-get install libterm-readline-perl-perl apt-utils -y
RUN apt-get install -y python3 python3-pip python3-virtualenv mlocate nginx
RUN pip3 install awscli flask boto3 uwsgi

RUN mkdir -p /opt/scripts /opt/dist /opt/conf
COPY start.sh /opt/scripts
RUN chmod 755 /opt/scripts/*.sh

VOLUME ['/opt/scripts', '/opt/dist', '/opt/conf']

EXPOSE 5000
EXPOSE 8080
EXPOSE 8081
EXPOSE 80
EXPOSE 443

# Consult the README.md (https://github.com/nicc777/flask-prod-docker) for an 
# explanation of all the environment variables
ENV DEBUG 0
ENV SYSLOG_SERVER 127.0.0.1
ENV SYSLOG_PORT 541
ENV SYSLOG_LEVEL ERROR
ENV AWS_DEFAULT_REGION us-east-1
ENV AWS_ACCESS_KEY_ID not-set
ENV AWS_SECRET_ACCESS_KEY not-set 
ENV APP_DIST /opt/dist/app.tar.gz
ENV UWSGI_CONF /opt/conf/app.ini
ENV UWSGI_SITE_CONF /opt/conf/app.conf
ENV APPLICATION_SCRIP_NAME app.py
ENV APPLICATION_CALLABLE_NAME app

CMD /opt/scripts/start.sh

