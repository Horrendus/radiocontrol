# What is "radiocontrol"

radiocontrol is a control & managment interface for [MPD](http://www.musicpd.org/), mostly to be used for the needs of internet streaming radio.
It was created because the existing control interfaces for streaming stations were not as flexible (usage of mpd, music preprocessing) as needed.

## Existing features (what it is capable of right now)

* Login (Users need to be created via django admin interface)
* Display scheduled playlists (playlists need to be added via django admin interface)
* Add new entries to the schedule and check for scheduling conflicts
* Start playing at the scheduled time via MPD

## Feature ideas (what it should be capable of, mostly in order of preference)

* add music to the MPD collection
* add playlists
* check if every song of the playlist is available in the MPD collection
* preprocess music (mp3gain, mixramp)
* public display of schedule
* better scheduling
* placeholder "playlists" for live streaming to icecast
* ...

# Requirements & Installation

## Requirements

* Python 3 (check requirements.txt for the Python dependencies)
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

If mpd is running in another docker image, you need to link it to this container.

```bash
docker run --name=radiocontrol --link radio:radio -e -e 'RADIO_MPD_HOST=radio' -e 'RADIO_MPD_PORT=6600' \
-e 'RADIO_SECRET_KEY=enter-secret-key-here' -d -it -p 443:443 -v /data/radiocontrol:/data radiocontrol
```

# Installation HowTo

# Author

* Stefan Derkits <stefan@derkits.at>

# License

If not otherwise stated, all code is licensed under the GNU Affero General Public License
