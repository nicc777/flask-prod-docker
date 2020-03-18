FROM ubuntu:latest
MAINTAINER Nico Coetzee <nicc777@gmail.com>

LABEL Description="A container for the production hosting of a flask application" Vendor="none" Version="0.1"

# Prep Python
RUN apt-get update && apt-get upgrade -y
RUN apt-get install libterm-readline-perl-perl apt-utils -y
RUN apt-get install -y python3 python3-pip
RUN pip3 install Flask Flask-Cognito gunicorn

# Install the app
WORKDIR /usr/src/app
RUN mkdir dist
COPY dist/*.tar.gz ./dist/
RUN pip3 install dist/*.tar.gz

# Operational Configuration
EXPOSE 8080
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8080", "--access-logfile", "-", "demo_api.app:app"]


