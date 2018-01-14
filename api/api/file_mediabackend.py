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

import base64
import os

from typing import Dict

from api.models import Song

MEDIA_ROOT = '/tmp/var/lib/mpd/'


def music_root():
    return MEDIA_ROOT + 'music/'


def playlist_root():
    return MEDIA_ROOT + 'playlists/'


def save_file(filename: str, file_data: bytes):
    print("save file", filename)
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'wb') as f:
        f.write(file_data)
    process_file(filename)


def validate(mediadata: Dict[str, str]):
    valid = list()
    valid.append('artist' in mediadata)
    valid.append('name' in mediadata)
    valid.append('filename' in mediadata)
    valid.append('data' in mediadata)
    return all(valid)


def process_file(filename: str):
    # Postprocessing of file, e.g. mp3gain
    pass


def save_media(mediadata: Dict[str, str]):
    ok = validate(mediadata)
    if ok:
        filename = mediadata['filename']
        base64_data_str = mediadata.pop('data')
        base64_data = bytes(base64_data_str, 'UTF-8')
        file_data = base64.b64decode(base64_data)
        full_filename = music_root() + filename
        save_file(full_filename, file_data)
        Song.objects.create(**mediadata)
        return True
    return False
