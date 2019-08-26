# REST API Backend for the Radiocontrol Project
#
# Copyright (C) 2017 Stefan Derkits <stefan@derkits.at>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os

from api.models import Song

from django.core.files.uploadedfile import UploadedFile

from mutagen import mp3

MEDIA_ROOT = '/tmp/var/lib/mpd/'


def music_root():
    return MEDIA_ROOT + 'music/'


def playlist_root():
    return MEDIA_ROOT + 'playlists/'


def process_file(filename: str):
    # Postprocessing of file, e.g. mp3gain
    pass


def create_song(full_filename: str) -> bool:
    tag = mp3.MP3(full_filename)
    filename = full_filename[len(music_root()):]
    t_artist = ""
    if 'TPE1' in tag:
        t_artist = tag['TPE1'].text[0].strip().lower()
    t_title = ""
    if 'TIT2' in tag:
        t_title = tag['TIT2'].text[0].strip().lower()
    if not t_artist and not t_title:
        return False
    length = tag.info.length
    Song.objects.create(artist=t_artist, title=t_title, filename=filename, length=length)
    return True


def save_media(file_data: UploadedFile) -> bool:
    print(f"Name: {file_data.name}, Type: {file_data.content_type}")
    print(type(file_data))
    full_filename = music_root() + file_data.name
    os.makedirs(os.path.dirname(full_filename), exist_ok=True)
    with open(full_filename, 'wb') as f:
        f.write(file_data.read())
    process_file(full_filename)
    if create_song(full_filename):
        # TODO: mpd update
        return True
    return False
