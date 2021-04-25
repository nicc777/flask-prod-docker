# Flask Production Docker Container

## What is this...

I experiment a lot so I needed an easy way to get [Flask](http://flask.pocoo.org/) applications ready for more production like environments.

Since I use a lot of [AWS Services](https://aws.amazon.com), especially [Cognito for user authentication](https://aws.amazon.com/cognito/), I have updated this project to reflect that integration.

## Requirements for Development on Local Machine

You should have the following installed on your local system:

* AWS CLI
* Python 3x, including pip (with some Linux distro's this may not come pre-installed)
* Terraform

Once you have cloned the Git repository, it's a good idea to set-up a Python virtual environment ad install some pre-requisites:

```bash
$ cd flask-prod-docker
$ python3 -m venv venv
$ source venv/bin/activate
(venv) $ pip3 install pylint boto3
```

Next, reefer to the [Cognito README](cognito/README.md) for instructions on preparing the Cognito User Pool.

Once you are done, ensure you are once again in the project root directory.

## Testing Locally

Assuming you have prepared the Cognito setup (see [the Cognito README](cognito/README.md)), set your environment variables:

```bash
(venv) $ export SECRET_KEY "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
(venv) $ export COGNITO_CLIENT_ID="xxxxxxxxxx"
(venv) $ export COGNITO_CLIENT_SECRET="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
(venv) $ export COGNITO_DOMAIN="xxxxxxxxxx"
(venv) $ export COGNITO_LOGIN_CALLBACK_URL="http://localhost:8080/cognito_callback"
(venv) $ export COGNITO_LOGOUT_CALLBACK_URL="http://localhost:8080/cognito_logout_callback"
```

_Just for clarity_: The `COGNITO_DOMAIN` is the value of `user_pool_domain_name` you obtained from the Terraform output. The other values should be self explanatory.

Then, as often as you modify your code, build the example app Docker image:

```bash
$ ./build.sh
```

Finally, test:

```bash
(venv) $ docker run -p 127.0.0.1:8080:8080                     \
--name example                                                 \
-e SECRET_KEY="$SECRET_KEY"                                    \
-e COGNITO_CLIENT_ID="$COGNITO_CLIENT_ID"                      \
-e COGNITO_CLIENT_SECRET="$COGNITO_CLIENT_SECRET"              \
-e COGNITO_DOMAIN="$COGNITO_DOMAIN"                            \
-e COGNITO_LOGIN_CALLBACK_URL="$COGNITO_LOGIN_CALLBACK_URL"    \
-e COGNITO_LOGOUT_CALLBACK_URL="$COGNITO_LOGOUT_CALLBACK_URL"  \
example-flask-cognito-app
```

Point your browser to [http://127.0.0.1:8080/](http://127.0.0.1:8080/)

