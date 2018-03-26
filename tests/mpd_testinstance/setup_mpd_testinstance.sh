#!/bin/bash
rm -r /tmp/var/
mkdir -p /tmp/var/lib/mpd/music/
mkdir -p /tmp/var/log/mpd/
touch /tmp/var/log/mpd/mpd.log
chown -R mpd:mpd /tmp/var/lib/mpd/
chown -R mpd:mpd /tmp/var/log/mpd/
chmod 777 /tmp/var/lib/mpd/music/
sudo -u mpd mpd --no-daemon mpd.conf
