# This file is part of radiocontrol.
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

import celery

from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete

from api.models import ScheduleEntry, ScheduleEntryOrder
from api.tasks import schedule_playlists


@receiver(post_save, sender=ScheduleEntryOrder, dispatch_uid='scheduleentry_order_postsave')
def entry_order_postsave_handler(*args, **kwargs):
    print(f"entry order postsave handler for schedule entry order called")
    instance = kwargs.get('instance')

    try:
        obj = ScheduleEntryOrder.objects.get(pk=instance.pk)
    except ScheduleEntryOrder.DoesNotExist:
        obj = instance

    se = obj.schedule_entry

    if se.task_id:
        celery.task.control.revoke(se.task_id)
        print(f"revoking task id: {se.task_id}")

    playlists = [playlist.name for playlist in se.playlists.all()]
    if playlists:
        print(f"entry order postsave: scheduling playlists: {playlists}")
        task = schedule_playlists.apply_async(eta=se.begin_datetime, kwargs={'playlists': playlists})
        se.task_id = task.id
        print(f"task id: {task.id}")
    else:
        se.task_id = ""
    se.save()


@receiver(post_delete, sender=ScheduleEntry, dispatch_uid='scheduleentry_postdelete')
def entry_postdelete_handler(*args, **kwargs):
    print(f"entry postdelete handler for schedule entry called")
    instance = kwargs.get('instance')

    if instance.task_id:
        celery.task.control.revoke(instance.task_id)
        print(f"revoking task id: {instance.task_id}")
