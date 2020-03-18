#!/bin/sh

# first build the python app
python3 setup.py sdist

# build te docker image
docker build --no-cache -t example-flask-cognito-app .

