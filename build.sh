#!/bin/sh

# first build the python app
rm -frR dist/
python3 setup.py sdist

# build te docker image
docker container rm example
docker build --no-cache -t example-flask-cognito-app .

