#!/usr/bin/env python3

# Script to upload a playlist & all it's songs to the radiocontrol API
#
# Copyright (C) 2018 Stefan Derkits <stefan@derkits.at>
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
# You should have received a copy of the GNU General Public License along with
# this program. If not, see <http://www.gnu.org/licenses/>.

import base64
import sys
import re
import os
import requests
import json

from mutagen.mp3 import MP3

from typing import Dict, Any

RADIOCONTROL_BASEURL = "http://localhost:8000/"

MUSIC_BASEDIR = "/var/lib/mpd/music/"


def parse_playlist(playlist_file: str):
    regex = re.compile("/.*/")
    files = [regex.sub("", line).strip() for line in open(playlist_file) if not line.startswith('#EXT')]
    tags = [line[line.index(",") + 1:] for line in open(playlist_file) if line.startswith('#EXTINF')]
    nok = 0
    nof = 0
    duration = 0
    songs = []

    for i in range(len(files)):
        f = MUSIC_BASEDIR + files[i]
        if f.lower().endswith("mp3"):
            f_artist = tags[i].split("-")[0].strip().lower()
            f_title = tags[i].split("-")[1].strip().lower()
            if os.path.isfile(f):
                tag = MP3(f)
                duration = duration + tag.info.length
                t_artist = ""
                if 'TPE1' in tag:
                    t_artist = tag['TPE1'].text[0].strip().lower()
                t_title = ""
                if 'TIT2' in tag:
                    t_title = tag['TIT2'].text[0].strip().lower()
                m_artist = t_artist == f_artist
                m_title = t_title == f_title
                if not (m_artist and m_title):
                    print("tag mismatch in %s: %s - %s vs. %s - %s" % (files[i], f_artist, f_title, t_artist, t_title))

                with open(f, "rb") as fp:
                    song_data = fp.read()
                    base64_data = base64.b64encode(song_data)
                    song = {
                        "artist": t_artist,
                        "name": t_title,
                        "filename": files[i],
                        "length": tag.info.length,
                        "data": str(base64_data, "UTF-8")
                    }
                    songs.append(song)
            else:
                print("%s (%s) doesn't exist" % (files[i], tags[i]))
                nof = nof + 1
    if nof:
        print(nof, " songs not found, not proceeding with upload")
        exit(1)
    return songs


def upload_song(song: Dict[str, Any]):
    upload_url = RADIOCONTROL_BASEURL + "media/"
    song_data = json.dumps(song)
    r = requests.post(upload_url, song_data)
    if not r.ok:
        print("error uploading song %s - %s" % (song["artist"], song["name"]))


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('Usage: read_and_upload_m3u.py filename.m3u')
        exit(1)
    filename = sys.argv[1]
    parsed_songs = parse_playlist(filename)
    for parsed_song in parsed_songs:
        upload_song(parsed_song)
