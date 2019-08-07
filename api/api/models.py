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

import enum

from typing import Dict

from django.db import models
from ordered_model.models import OrderedModel


class SongStatus(enum.Enum):
    OK = "OK"
    WARN = "WARNING"
    ERROR = "ERROR"


class Song(models.Model):
    artist = models.CharField(max_length=128)
    title = models.CharField(max_length=128)
    filename = models.CharField(max_length=256, unique=True)
    length = models.IntegerField()
    song_status = models.CharField(max_length=255, choices=[(status.name, status.value) for status in SongStatus])


class Playlist(models.Model):
    name = models.CharField(max_length=128, unique=True)
    songs = models.ManyToManyField(Song, through="PlaylistOrder")

    @property
    def length(self) -> float:
        return sum([song.length for song in self.songs.all()])

    @property
    def status(self) -> SongStatus:
        states = [song.song_status for song in self.songs.all()]
        if SongStatus.ERROR in states:
            return SongStatus.ERROR
        elif SongStatus.WARN in states:
            return SongStatus.WARN
        else:
            return SongStatus.OK

    def __unicode__(self):
        return f"{self.name}"


class PlaylistOrder(OrderedModel):
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE)
    song = models.ForeignKey(Song, on_delete=models.CASCADE)

    class Meta:
        order_with_respect_to = 'playlist'


# distinct entry in the schedule (from pause to pause)
class ScheduleEntry(models.Model):
    begin_datetime = models.DateTimeField(max_length=128, unique=True)
    playlists = models.ManyToManyField(Playlist, through='ScheduleEntryOrder')
    task_id = models.CharField(max_length=256)

    # this method is on the model's manager
    @staticmethod
    def get_closest_to(target_datetime) -> Dict[str, 'ScheduleEntry']:
        closest_after = ScheduleEntry.objects.filter(begin_datetime__gt=target_datetime).order_by('begin_datetime')
        closest_before = ScheduleEntry.objects.filter(begin_datetime__lt=target_datetime).order_by('-begin_datetime')

        closest_entries = {
            'before': closest_before.first(),
            'after': closest_after.first()
        }
        return closest_entries

    @property
    def length(self):
        return sum([playlist.length for playlist in self.playlists.all()])


class ScheduleEntryOrder(OrderedModel):
    schedule_entry = models.ForeignKey(ScheduleEntry, on_delete=models.CASCADE)
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE)

    class Meta:
        order_with_respect_to = 'schedule_entry'
