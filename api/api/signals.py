# This file is part of radiocontrol.
#
# Copyright (C) 2017 - 2019 Stefan Derkits <stefan@derkits.at>
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

from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save, post_delete, pre_delete

from api.models import (
    Song,
    PlaylistEntry,
    ScheduleEntry,
    MPDTask,
    MPDTaskScheduleEntryOrder,
)
from api import tasks


@receiver(post_save, sender=Song, dispatch_uid="song_postsave")
@receiver(post_delete, sender=Song, dispatch_uid="song_postdelete")
def song_postsave_postdelete_handler(*args, **kwargs):
    print("song postsave handler called")
    song = kwargs.get("instance")
    playlist_entries = PlaylistEntry.objects.filter(filename=song.filename)
    for playlist_entry in playlist_entries:
        playlist_entry.save()


@receiver(pre_save, sender=PlaylistEntry, dispatch_uid="playlistentry_postsave")
def playlistentry_postsave_handler(*args, **kwargs):
    print("playlistentry postsave handler called")
    playlist_entry = kwargs.get("instance")
    playlist_entry.compute_status()


@receiver(post_save, sender=ScheduleEntry, dispatch_uid="scheduleentry_postsave")
def entry_postsave_handler(*args, **kwargs):
    instance = kwargs.get("instance")
    try:
        schedule_entry = ScheduleEntry.objects.get(pk=instance.pk)
    except ScheduleEntry.DoesNotExist:
        schedule_entry = instance

    closest_schedule_entries = schedule_entry.get_closest_to(
        schedule_entry.begin_datetime
    )
    if (
        closest_schedule_entries["before"]
        and closest_schedule_entries["after"]
        and schedule_entry.begin_datetime
        == closest_schedule_entries["before"].end_datetime
        and schedule_entry.end_datetime
        == closest_schedule_entries["after"].begin_datetime
    ):
        # special case: ScheduleEntry is exactly between previous & next ScheduleEntries
        # TODO: get mpd task id of previous & next entry
        # TODO: case 1: previous entry already started playing
        # TODO: case 2: previous entry starts playing in the future
        return
    if (
        closest_schedule_entries["before"]
        and schedule_entry.begin_datetime
        == closest_schedule_entries["before"].end_datetime
    ):
        # special case: ScheduleEntry is exactly after previous ScheduleEntry
        # TODO: get mpd task id of previous entry
        # TODO: case 1: previous entry already started playing
        # TODO: case 2: previous entry starts playing in the future
        # TODO: add playlists without using celery
        # TODO: add this playlist to mpd task id (of previous entry)
        return
    if (
        closest_schedule_entries["after"]
        and schedule_entry.end_datetime
        == closest_schedule_entries["after"].begin_datetime
    ):
        # special case: ScheduleEntry is exactly before next ScheduleEntry
        # TODO: get mpd task id of next entry
        # TODO: revoke mpd task id of next entry
        # TODO: new mpd task: this playlist + all playlists of revoked mpd task
        return

    # simple case: ScheduleEntry is independent from the one before & the one after
    celery_task = tasks.schedule_playlists.apply_async(
        eta=schedule_entry.begin_datetime,
        kwargs={"playlists": [schedule_entry.playlist.name]},
    )
    mpd_task = MPDTask.objects.create(task_id=celery_task.id)
    MPDTaskScheduleEntryOrder.objects.create(
        schedule_entry=schedule_entry, mpd_task=mpd_task
    )


@receiver(pre_delete, sender=ScheduleEntry, dispatch_uid="scheduleentry_predelete")
def entry_predelete_handler(*args, **kwargs):
    instance = kwargs.get("instance")
    try:
        schedule_entry = ScheduleEntry.objects.get(pk=instance.pk)
    except ScheduleEntry.DoesNotExist:
        schedule_entry = instance

    closest_schedule_entries = schedule_entry.get_closest_to(
        schedule_entry.begin_datetime
    )

    # TODO: if ScheduleEntry is mpd taks with only this playlist, then revoke
    # TODO: if ScheduleEntry is part of an mpd task with more entries:
    # TODO: case 1: ScheduleEntry is at the beginning (or end) and mpd task start time is in the future
    # TODO: revoke mpd task, create new task without this entry
    # TODO: case 2: ScheduleEntry is somewhere in the middle and mpd task start time is in the future
    # TODO: revoke mpd task, create new tasks: one with playlists before this playlist & one with playlist after this
    # TODO: special cases: MPD task (playing of playlists before this one) already started
