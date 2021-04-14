FROM ubuntu:groovy-20210325

LABEL Description="A container for the production hosting of a flask application" Vendor="none" Version="0.1"

# Prep Python
RUN apt-get update && apt-get upgrade -y
RUN apt-get install libterm-readline-perl-perl apt-utils -y
RUN apt-get install -y python3 python3-pip
RUN pip3 install Flask Flask-Cognito gunicorn cognitojwt

