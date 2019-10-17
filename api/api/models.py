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


class Song(models.Model):
    artist = models.CharField(max_length=128)
    title = models.CharField(max_length=128)
    filename = models.CharField(max_length=256, unique=True)
    length = models.FloatField()


class PlaylistEntryStatus(enum.Enum):
    OK = "OK"
    WARN = "WARNING"
    ERROR = "ERROR"


class PlaylistEntry(models.Model):
    artist = models.CharField(max_length=128)
    title = models.CharField(max_length=128)
    filename = models.CharField(max_length=256)
    pe_length = models.IntegerField()
    status = models.CharField(
        max_length=255,
        choices=[(status.name, status.value) for status in PlaylistEntryStatus],
    )
    song = models.ForeignKey(Song, null=True, on_delete=models.SET_NULL)

    class Meta:
        unique_together = ("artist", "title", "filename", "pe_length")

    @property
    def length(self) -> float:
        if self.status == str(PlaylistEntryStatus.ERROR):
            return self.pe_length
        return self.song.length

    def compute_status(self):
        try:
            song = Song.objects.get(filename=self.filename)
            self.song = song
            if (
                song.artist.lower() == self.artist.lower()
                and song.title.lower() == self.title.lower()
                and int(song.length) == self.pe_length
            ):
                self.status = str(PlaylistEntryStatus.OK)
            else:
                self.status = str(PlaylistEntryStatus.WARN)
        except models.ObjectDoesNotExist:
            self.status = str(PlaylistEntryStatus.ERROR)

    def update_status(self):
        self.compute_status()
        self.save()


class Playlist(models.Model):
    name = models.CharField(max_length=128, unique=True)
    entries = models.ManyToManyField(PlaylistEntry, through="PlaylistOrder")

    @property
    def length(self) -> float:
        return sum([entry.length for entry in self.entries.all()])

    @property
    def status(self) -> str:
        states = [entry.status for entry in self.entries.all()]
        error_state = str(PlaylistEntryStatus.ERROR)
        warn_state = str(PlaylistEntryStatus.WARN)
        ok_state = str(PlaylistEntryStatus.OK)
        if error_state in states:
            return error_state
        elif warn_state in states:
            return warn_state
        else:
            return ok_state

    def __str__(self):
        return f"{self.name}"


class PlaylistOrder(OrderedModel):
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE)
    entry = models.ForeignKey(PlaylistEntry, on_delete=models.CASCADE)

    class Meta:
        order_with_respect_to = "playlist"


class MPDTask(models.Model):
    begin_datetime = models.DateTimeField(unique=True)
    playlists = models.ManyToManyField(Playlist, through="MPDTaskPlaylistOrder")


class MPDTaskPlaylistOrder(OrderedModel):
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE)
    mpd_task = models.ForeignKey(MPDTask, on_delete=models.CASCADE)

    class Meta:
        order_with_respect_to = "playlist"


class ScheduleEntry(models.Model):
    begin_datetime = models.DateTimeField(unique=True)
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE)

    # this method is on the model's manager
    @staticmethod
    def get_closest_to(target_datetime) -> Dict[str, "ScheduleEntry"]:
        closest_after = ScheduleEntry.objects.filter(
            begin_datetime__gt=target_datetime
        ).order_by("begin_datetime")
        closest_before = ScheduleEntry.objects.filter(
            begin_datetime__lt=target_datetime
        ).order_by("-begin_datetime")

        closest_entries = {
            "before": closest_before.first(),
            "after": closest_after.first(),
        }
        return closest_entries

    @property
    def length(self):
        return self.playlist.length
