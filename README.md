# Flask Production Docker Container

## What is this...

I experiment a lot so I needed an easy way to get [Flask](http://flask.pocoo.org/) applications ready for more production like environments.

## AWS

Since I use a lot of [AWS Services](https://aws.amazon.com), especially [Cognito for user authentication](https://aws.amazon.com/cognito/), I have updated this project to reflect that integration.

## Deployment

The Docker image will be made available in the public Docker repository... `TODO`

# Usage

Coming shortly...

## Testing Locally

First, you will need to build the base docker image. It uses the official Docker Ubuntu image and installs the required packages so that you don't have to do it every time when building the application Docker image. This is typically a once of exercise on your local machine:

```bash
$ docker image rm example-flask-cognito-base
$ cd docker/base
$ docker build --no-cache -t example-flask-cognito-base .
$ cd $OLDPWD
```

Then, as often as you modify your code, build the example app Docker image:

```bash
$ ./build.sh
```

Finally, test:

```bash
$ docker run -p 127.0.0.1:8080:8080 --name example example-flask-cognito-app
```

Point your browser to [http://127.0.0.1:8080/](http://127.0.0.1:8080/)

