FROM python:3.10.4-alpine3.15

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1

COPY . /app

RUN apk update \
  && apk add --virtual build-deps gcc musl-dev \
  && apk add --no-cache \
    postgresql-dev \
    libffi-dev \
    py-cffi \
    gettext \
    postgresql-client \
    libpq-dev \
    py3-gunicorn \
  && apk add --no-cache --virtual .build-deps-edge --repository http://dl-cdn.alpinelinux.org/alpine/edge/testing \
    gdal-dev \
    geos-dev \
    proj-dev \
  && pip install --no-cache-dir --upgrade pip \
  && pip install --no-cache-dir virtualenv \
  && virtualenv /env \
  && /env/bin/pip install --no-cache-dir --upgrade pip \
  && /env/bin/pip install -r /app/requirements-dev.txt \
  && rm -rf /root/.cache

RUN adduser -D -H backoffice_user \
  && mkdir -p /app/log \
  && touch /app/log/shuttleapp.log \
  && chown -R backoffice_user:backoffice_user /app \
  && chmod +x /app/docker/entrypoint.sh

EXPOSE 8091

CMD ["/app/docker/entrypoint.sh"]
