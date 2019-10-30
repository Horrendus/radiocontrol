FROM python:3.8

RUN pip install -U redis pipenv uwsgi

ENV ENVIRONMENT "dev"

COPY Pipfile* /srv/
WORKDIR /srv
RUN pipenv install --system
COPY . /srv

WORKDIR /srv/
RUN rm -f db.sqlite3
RUN ./manage.py migrate

EXPOSE 80
