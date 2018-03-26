# REST API Backend for the Radiocontrol Project
#
# Copyright (C) 2018 Stefan Derkits <stefan@derkits.at>
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

from mpd import MPDClient

from api.models import Song, Playlist, PlaylistOrder


def main() -> None:
    print("starting MPD import")
    client = MPDClient()
    client.connect("localhost", 6600)
    print("client connected")

    songs_mpd = client.listallinfo()

    playlist_names = [p["playlist"] for p in client.listplaylists()]

    playlists_mpd = [{
        "name": playlist_name,
        "songs": [s["file"] for s in client.listplaylistinfo(playlist_name)]
    } for playlist_name in playlist_names]

    songs = [Song(
        **{
            "title": s["title"],
            "artist": s["artist"],
            "length": s["time"],
            "filename": s["file"]
        }) for s in songs_mpd]

    Song.objects.bulk_create(songs)
    print("songs bulk created")

    for mpd_playlist in playlists_mpd:
        playlist = Playlist.objects.create(name=mpd_playlist["name"])
        for song_filename in mpd_playlist["songs"]:
            song = Song.objects.get(filename=song_filename)
            PlaylistOrder.objects.create(playlist=playlist, song=song)


if __name__ == "__main__":
    main()
