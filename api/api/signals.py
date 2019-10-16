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
from django.db.models.signals import pre_save, post_save, post_delete

from api.models import Song, PlaylistEntry


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
