# What is "radiocontrol"

radiocontrol is a control & managment interface for [MPD](http://www.musicpd.org/), mostly to be used for the needs of internet streaming radio.
It was created because the existing control interfaces for streaming stations were not as flexible (usage of mpd, music preprocessing) as needed.

## Existing features (what it is capable of right now)

* add music to the MPD collection
* add playlists (only via JSON atm)
* Display scheduled playlists (playlists need to be added via django admin interface)
* Add new entries to the schedule and check for scheduling conflicts
* Start playing at the scheduled time via MPD
* Remove

## Feature ideas (what it should be capable of, mostly in order of preference)

* Authentication
* upload playlists as m3u or xspf
* preprocess music (mp3gain, mixramp)
* public display of schedule
* better scheduling
** remove not yet started playlists when first playlist has already started
** stop current playlist at some predefined moment
* placeholder "playlists" for live streaming to icecast
* ...

# Project Structure

* api: Django 2.0 REST API - under development - rewrite of the old App (mostly) from scratch, will only offer a REST API
* frontends: diverse frontends for the API
* old_radiocontrol_app: old Django 1 Application that supports some features with a basic HTML frontend

## Frontends

* qml_pyside: Frontend using QML - under development - Dependencies: Python 3.0, PySide 2, Qt5

# Requirements & Installation

## Requirements

* Python 3 (check requirements.txt/Pipfile for Python dependencies)
* rabbitmq (for celery)
* mpd

# Installation

## Docker

The preferred & tested installation of this application is in a Docker container.

### Build image

To build the container image use the following command:

```bash
docker docker build -t radiocontrol:latest
```

### Data directory

Create a data directory (used to store the radiocontrol & celery databases). From now on the data directory will be referenced as **/data/radiocontrol**

### SSL

When run in production mode, this application requires SSL. If you don't have a certificate & key yet, use the following commands to generate them:

```bash
openssl genrsa -out radiocontrol.key 2048
openssl req -new -key radiocontrol.key -out radiocontrol.csr
openssl x509 -req -days 3650 -in radiocontrol.csr -signkey radiocontrol.key -out radiocontrol.crt
```

The configuration expects *radiocontrol.key* & *radiocontrol.crt* to be in the **/data/radiocontrol/certs/** directory.

### Run image

If mpd is running in another docker image, you need to link it to this container. Also if rabbitmq is running in another container, link that one to.

```bash
docker run --name=radiocontrol --link mpd:mpd --link rabbitmq:rabbitmq -e -e 'RADIO_MPD_HOST=radio' -e 'RADIO_MPD_PORT=6600' \
-e 'RADIO_SECRET_KEY=enter-secret-key-here' -e 'RADIO_BROKER_URL=amqp://guest:guest@rabbitmq:5672//' \
-e 'DJANGO_SETTINGS_MODULE=radiocontrol.settings.production' -d -it -p 443:443 -v /data/radiocontrol:/data radiocontrol
```

# Author

* Stefan Derkits <stefan@derkits.at>

# License

If not otherwise stated, all code is licensed under the GNU Affero General Public License
