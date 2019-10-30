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
    files = [
        regex.sub("", line).strip()
        for line in open(playlist_file)
        if not line.startswith("#EXT")
    ]
    tags = [
        line[line.index(",") + 1 :]
        for line in open(playlist_file)
        if line.startswith("#EXTINF")
    ]
    nok = 0
    nof = 0
    duration = 0

    for i in range(len(files)):
        f = MUSIC_BASEDIR + files[i]
        if f.lower().endswith("mp3"):
            f_artist = tags[i].split("-")[0].strip().lower()
            f_title = tags[i].split("-")[1].strip().lower()
            if os.path.isfile(f):
                tag = MP3(f)
                duration = duration + tag.info.length
                t_artist = ""
                if "TPE1" in tag:
                    t_artist = tag["TPE1"].text[0].strip().lower()
                t_title = ""
                if "TIT2" in tag:
                    t_title = tag["TIT2"].text[0].strip().lower()
                m_artist = t_artist == f_artist
                m_title = t_title == f_title
                if not (m_artist and m_title):
                    print(
                        "tag mismatch in %s: %s - %s vs. %s - %s"
                        % (files[i], f_artist, f_title, t_artist, t_title)
                    )
                upload_song(f)
    if nof:
        print(nof, " songs not found, not proceeding with upload")
        exit(1)


def upload_song(song: str):
    upload_url = RADIOCONTROL_BASEURL + "media/"
    r = requests.post(upload_url, files={"data": open(song, "rb")})
    if not r.ok:
        print(f"error uploading song {song}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: read_and_upload_m3u.py filename.m3u")
        exit(1)
    filename = sys.argv[1]
    if len(sys.argv) >= 3:
        RADIOCONTROL_BASEURL = sys.argv[2]
    parse_playlist(filename)
