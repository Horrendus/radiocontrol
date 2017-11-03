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

from django.db import models


class Song(models.Model):
    artist = models.CharField()
    name = models.CharField()
    file = models.FileField(upload_to='music/')


class Playlist(models.Model):
    name = models.CharField()
    songs = models.ManyToManyField(Song)


# distinct entry in the schedule (from pause to pause)
class ScheduleEntry(models.Model):
    begin_datetime = models.DateTimeField()
    playlists = models.ManyToManyField(Playlist, through='PlaylistOrder')


class PlaylistOrder(models.Model):
    number = models.PositiveIntegerField()
    schedule_entry = models.ForeignKey(ScheduleEntry)
    playlist = models.ForeignKey(Playlist)


# songs that may not yet be available
class DraftSong(models.Model):
    artist = models.CharField()
    name = models.CharField()
    filename = models.CharField()


# generated from uploaded playlists and not all songs may yet be available
# when all songs are available, it can be stored as a Playlist
class DraftPlaylist(models.Model):
    name = models.CharField()
    songs = models.ManyToManyField(DraftSong)
