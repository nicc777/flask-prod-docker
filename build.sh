#!/bin/sh

# first build the python app
rm -frR dist/
python3 setup.py sdist

# build te docker image
docker container rm example
rm -frR docker/example/dist
mkdir docker/example/dist
cp -vf dist/* docker/example/dist/
cd docker/example
docker build --no-cache -t example-flask-cognito-app .

