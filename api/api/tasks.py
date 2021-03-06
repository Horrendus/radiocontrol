# REST API Backend for the Radiocontrol Project
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

from celery import shared_task
from django.conf import settings
from mpd import MPDClient

from typing import List


@shared_task
def schedule_playlists(playlists: List[str], append=False):
    client = MPDClient()
    client.connect(settings.MPD_SERVER, settings.MPD_PORT)
    if not append:
        client.clear()
    print(f"Celery Task scheduling playlists {playlists}")
    for playlist in playlists:
        client.load(playlist)
    if not append:
        client.play(0)
    client.close()
    client.disconnect()
