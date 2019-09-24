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
import re

from api.models import Song, PlaylistEntry, Playlist, PlaylistOrder

from django.core.files.uploadedfile import UploadedFile

from mutagen import mp3

from typing import Tuple, List

MEDIA_ROOT = '/tmp/var/lib/mpd/'

EXTINF = "#EXTINF"


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


def save_playlist(file_data: UploadedFile) -> bool:
    print(f"Name: {file_data.name}, Type: {file_data.content_type}")
    full_playlist_name, file_extension = os.path.splitext(file_data.name)
    playlist_name = os.path.basename(full_playlist_name)
    if file_extension.lower() != ".m3u":
        print("unsupported file type")
        return False
    playlist_content = file_data.read()
    full_filename = playlist_root() + os.path.basename(file_data.name)
    os.makedirs(os.path.dirname(full_filename), exist_ok=True)
    with open(full_filename, 'wb') as f:
        f.write(playlist_content)
    ok, playlist_entries = parse_m3u_playlist(str(playlist_content,"UTF-8").split('\n'))
    if not ok:
        print("failed parsing playlist")
        return False
    p = Playlist.objects.create(name=playlist_name)
    for entry in playlist_entries:
        pe, _ = PlaylistEntry.objects.get_or_create(playlist=p, length=entry[0], artist=entry[1], title=entry[2],
                                                    filename=entry[3])
        PlaylistOrder.objects.create(playlist=p, entry=pe)
    return True


def parse_m3u_playlist(playlist_content) -> Tuple[bool, List[Tuple[int, str, str, str]]]:
    if playlist_content[0] != "#EXTM3U":
        print("only EXTM3U format supported")
        return False, []
    # TOOD: using os basename() should be easier than this regex substitution
    regex = re.compile("/.*/")
    files = [regex.sub("", line).strip() for line in playlist_content if line and not line.startswith('#EXT')]
    print("Files: ", files)
    tags = [line for line in playlist_content if line.startswith(EXTINF)]
    print("Tags: ", tags)
    playlist_entries = []
    if len(files) != len(tags):
        print("invalid playlist, different number of tags & files")
        return False, []
    for i in range(len(tags)):
        ok, length, artist, title = parse_m3u_playlist_entry(tags[i])
        if not ok:
            print("couldnt parse playlist tag entry")
            return False, []
        playlist_entries.append((length, artist, title, files[i]))
    return True, playlist_entries


def parse_m3u_playlist_entry(tag: str) -> Tuple[bool, int, str, str]:
    print(tag)
    # TODO: this whole function would work better with regexes
    if len(tag) < len(EXTINF)+1:
        print("invalid extinft line: too short")
        return False, -1, "", ""
    else:
        tag = tag[len(EXTINF)+1:]
        length_seperator_position = tag.find(",")
        if length_seperator_position == -1:
            print("invalid extinf line: no length seperator found")
            return False, -1, "", ""
        length_str = tag[:length_seperator_position]
        if not length_str.isdigit():
            print("invalid extinf line: length not an integer")
            return False, -1, "", ""
        length = int(length_str)
        artist_seperator_position = tag.find("-")
        if artist_seperator_position == -1:
            print("invalid extinf line: no artist seperator found")
            return False, -1, "", ""
        if len(tag) < (artist_seperator_position + 2):
            print("invalid extinf line: tag doesnt have title")
            return False, -1, "", ""
        artist = tag[length_seperator_position+1:artist_seperator_position].strip()
        title = tag[artist_seperator_position+1:].strip()
        if not artist or not title:
            print("invalid extinf line: artist or title empty")
            return False, -1, "", ""
        return True, length, artist, title
