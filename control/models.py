# This file is part of radiocontrol.
#
# Copyright (C) 2015 Stefan Derkits <stefan@derkits.at>
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
from django.utils import timezone
from django.core.exceptions import ValidationError

from datetime import datetime, timedelta


class Playlist(models.Model):
    name = models.TextField(max_length=30)
    filename = models.TextField(max_length=30, unique=True)
    duration = models.DurationField()

    def __str__(self):
        return self.name


class ScheduleEntry(models.Model):
    begin_time = models.DateTimeField()
    playlist = models.ForeignKey(Playlist)
    task_id = models.CharField(max_length=256)

    def _get_end_time(self):
        return self.begin_time + self.playlist.duration

    end_time = property(_get_end_time)

    def clean(self):
        print("model clean")
        if timezone.now() > (self.begin_time - timedelta(seconds=1)): #TODO: change timedelta to 30 min
            raise ValidationError("Must schedule 1 second in advance")

        next = ScheduleEntry.objects.filter(begin_time__gte=self.begin_time).order_by("begin_time").first()
        if next is not None:
            if next.begin_time < self.end_time:
                raise ValidationError("Scheduling Conflict: End time before begin time of the next entry")
        last = ScheduleEntry.objects.filter(begin_time__lte=self.begin_time).order_by("-begin_time").first()
        if last is not None:
            if self.begin_time < last.end_time:
                raise ValidationError("Scheduling Conflict: Begin time before end time of the previous entry")
