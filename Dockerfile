FROM python:3

RUN apt-get update && apt-get install -y rabbitmq-server

RUN pip install uwsgi

COPY . /srv
WORKDIR /srv

RUN pip install -r requirements.txt

ENV ENVIRONMENT "dev"

RUN ["/bin/bash", "scripts/setup.sh"]

CMD ["/bin/bash", "scripts/startup.sh"]

EXPOSE 80
