# WolfBeacon Core API

WolfBeacon's Core API for Mobile and Analytics.

Written in [Python 3](https://www.python.org/downloads/release/python-352/), powered by [Django](https://www.djangoproject.com/), [Django Rest Framework](http://www.django-rest-framework.org/), [PostgreSQL](https://www.postgresql.org/) and [Auth0](https://auth0.com).

## API Documentation

API Documentation is available at **[https://api.wolfbeacon.com/docs](https://api.wolfbeacon.com/docs)**.

Docs are generated using [apidoc](http://apidocjs.com/). Doc strings are present in views under the `/api/views` directory. Documentation is served separately by the [wolfbeacon-apidoc-gen](https://github.com/wolfbeacon/wolfbeacon-apidoc-gen) service.


## Local Development Setup

* [Install virtualenv supporting Python 3.5](https://stackoverflow.com/questions/29934032/virtualenv-python-3-ubuntu-14-04-64-bit) and activate it

  `virtualenv venv && source venv/bin/activate`
* Make a *settings.py* file from the *settings.template.py* file provided

  `cp wolfbeacon/settings.template.py wolfbeacon/settings.py`

* Add the *SECRET_KEY*, *DATABASES* and *AUTH0* configuration in the *settings.py* file.

  Adding the *AUTH0* configuration (used for [Auth0](https://auth0.com) Token Validation) is optional. Hence for local testing, disable it by removing `'api.middleware.auth0.Auth0Middleware',` from *MIDDLEWARE*.

* Install the requirements

  `sudo pip install -r requirements.txt`

* Make the Database Migrations

  `python manage.py migrate`

* Run the development server

  `python manage.py runserver`


## Running in Production with Docker

Make sure [Docker](https://docs.docker.com/engine/installation/) is installed on your system. We run this API a Dockerized application in production.

Assuming Postgres is already running in a separate container remotely accessible and the *settings.py* file is all configured, we are ready to go. Simply build a docker image for this application and run it.

* `sudo docker build -t wolfbeacon-core-api .`
* `sudo docker run -p 8000:8000 wolfbeacon-core-api`

This should have have your app up and running, accessible on port 8000.

## Simulating Production Environment

For testing purposes, a production environment can be simulated using the *docker-compose* file provided which bundles the API and Postgres together.

It uses a slightly modified Dockerfile alongwith an entrypoint, both located in `/.docker-compose/`

* `cp wolfbeacon/settings.docker-compose.py wolfbeacon/settings.py`

* `sudo docker-compose up --build -d`


