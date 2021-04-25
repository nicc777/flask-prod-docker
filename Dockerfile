FROM ubuntu:21.04 AS flask-prod-base

LABEL Description="A container for the production hosting of a flask application" Vendor="none" Version="0.1"

# Prep Python
ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get upgrade -y
RUN apt-get install libterm-readline-perl-perl apt-utils -y
RUN apt-get install -y python3 python3-pip
RUN pip3 install Flask Flask-Cognito gunicorn cognitojwt




FROM flask-prod-base

LABEL Description="A container for the production hosting of a flask application" Vendor="none" Version="0.1"

# Envieonment
ENV SECRET_KEY "Not a very strong secret"
ENV COGNITO_CLIENT_ID not-set
ENV COGNITO_CLIENT_SECRET not-set
ENV COGNITO_DOMAIN not-set
ENV COGNITO_LOGIN_CALLBACK_URL not-set
ENV COGNITO_LOGOUT_CALLBACK_URL not-set
ENV COGNITO_SCOPE "openid+profile"
ENV COGNITO_STATE "DEMO-STATE"

# Install the app
WORKDIR /usr/src/app
RUN mkdir dist
COPY dist/*.tar.gz ./dist/
RUN pip3 install dist/*.tar.gz

# Operational Configuration
EXPOSE 8080
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8080", "--access-logfile", "-", "example.example:app"]


