# What is "radiocontrol"

radiocontrol is a control & managment interface for [MPD](http://www.musicpd.org/), mostly to be used for the needs of internet streaming radio.
It was created because the existing control interfaces for streaming stations were not as flexible (usage of mpd, music preprocessing) as needed.

## Existing features (what it is capable of right now)

Note: this lists the features of the backend. Not all is yet accessible via frontend or scripts

* add music to the MPD collection
* add playlists (as m3u)
* Status check of playlists (do the files exist? are the tags as expected?)
* get schedule entries
* Add new entries to the schedule and check for scheduling conflicts
* Start playing at the scheduled time via MPD

## Feature ideas (what it should be capable of, mostly in order of preference)

* preprocess music (mp3gain, mixramp)
* remove or change playlists
* schedule & remove playlists by name
* remove schedule entries
* better scheduling
** see TODOs (schedule playlists after, before, in-between existing schedule entries)
* allow more flexible backend settings, seperate debug from production settings
* upload playlists as xspf
* Authentication
* placeholder schedule entries for live streaming to icecast
* ...

# Project Structure

* api: Django 2.0 REST API - under development
* frontends: diverse frontends for the API

## Frontends

* web: Vue.js 2.0 frontend - under Development
* python_cmdline: Python scripts to access the API

# Requirements & Installation

## Requirements

* Python 3 (check Pipfile for Python dependencies)
* redis (for celery)
* mpd

# Installation

## Docker

The preferred & tested installation of this application is in a Docker container.

### Build image

To build the container for the API image use the following command:

```bash
cd api
docker docker build -t radiocontrol_api:latest
```

### Run image

MPD Server can be set via environment variables in the API container.

The example docker-compose.yml file in this project starts Redis & Celery and uses the MPD server on the host.

# Similar projects

* LibreTime: https://github.com/LibreTime/libretime
* AuRa: https://gitlab.servus.at/autoradio
* AzuraCast: https://github.com/AzuraCast/AzuraCast


# Author

* Stefan Derkits <stefan@derkits.at>

# License

If not otherwise stated, all code is licensed under the GNU Affero General Public License
