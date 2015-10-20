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

import celery

from control.models import ScheduleEntry
from control.tasks import schedule_playlist
from django.dispatch import receiver
from django.db.models.signals import pre_save, pre_delete


@receiver(pre_save, sender= ScheduleEntry, dispatch_uid='scheduleentry_presave')
def entry_presave_handler(*args, **kwargs):
    instance = kwargs.get('instance')
    try:
        obj = ScheduleEntry.objects.get(pk=instance.pk)
    except ScheduleEntry.DoesNotExist:
        obj = instance

    if obj.task_id:
        celery.task.control.revoke(obj.task_id)

    task = schedule_playlist.apply_async(eta = instance.begin_time, kwargs={'playlist_name': instance.playlist.filename} )
    instance.task_id = task.id


@receiver(pre_delete, sender= ScheduleEntry, dispatch_uid='scheduleentry_predelete')
def entry_predelete_handler(*args, **kwargs):
    instance = kwargs.get('instance')
    try:
        obj = ScheduleEntry.objects.get(pk=instance.pk)
    except ScheduleEntry.DoesNotExist:
        obj = instance

    celery.task.control.revoke(obj.task_id)