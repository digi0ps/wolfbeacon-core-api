FROM python:3.5-alpine

ADD requirements.txt /requirements.txt

# Install build deps, then run `pip install`
# Then, remove unneeded build deps all in a single step
RUN set -ex \
    && apk add --no-cache --virtual .build-deps \
            gcc \
            make \
            libc-dev \
            musl-dev \
            linux-headers \
            pcre-dev \
            postgresql-dev \
    && pyvenv /venv \
    && /venv/bin/pip install -U pip \
    && LIBRARY_PATH=/lib:/usr/lib /bin/sh -c "/venv/bin/pip install --no-cache-dir -r /requirements.txt" \
    && runDeps="$( \
            scanelf --needed --nobanner --recursive /venv \
                    | awk '{ gsub(/,/, "\nso:", $2); print "so:" $2 }' \
                    | sort -u \
                    | xargs -r apk info --installed \
                    | sort -u \
    )" \
    && apk add --virtual .python-rundeps $runDeps \
    && apk del .build-deps

# Install npm for apidoc
RUN apk add --update nodejs nodejs-npm
RUN npm install apidoc -g

# Run apidoc
RUN apidoc -i api/routes -o docs

# Copy application code to the container
RUN mkdir /code/
WORKDIR /code/
ADD . /code/

# Make DB Migrations
RUN python manage.py makemigrations api
RUN python manage.py migrate

# uWSGI will listen on this port
EXPOSE 8000

# uWSGI configuration:
ENV UWSGI_VIRTUALENV=/venv UWSGI_WSGI_FILE=wolfbeacon/wsgi.py UWSGI_HTTP=:8000 UWSGI_MASTER=1 UWSGI_WORKERS=2 UWSGI_THREADS=8 UWSGI_UID=1000 UWSGI_GID=2000 UWSGI_LAZY_APPS=1 UWSGI_WSGI_ENV_BEHAVIOR=holy

# Start uWSGI
CMD ["/venv/bin/uwsgi", "--http-auto-chunked", "--http-keepalive"]