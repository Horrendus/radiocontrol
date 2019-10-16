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

from django.contrib import admin
from django.urls import path

from api.views import (
    SongListView,
    PlaylistListCreateView,
    PlaylistReadUpdateDestroyView,
    MediaCreateView,
    MediaReadUpdateDestroyView,
    ScheduleEntryListView,
    ScheduleEntryReadDestroyView,
    ScheduleEntryCreateView,
)

urlpatterns = [
    path("songs/", SongListView.as_view()),
    path("playlist/<str:name>/", PlaylistReadUpdateDestroyView.as_view()),
    path("playlists/", PlaylistListCreateView.as_view()),
    path("media/", MediaCreateView.as_view()),
    path("media/<str:filename>/", MediaReadUpdateDestroyView.as_view()),
    path("scheduleentries/", ScheduleEntryListView.as_view()),
    path("scheduleentry/<int:id>/", ScheduleEntryReadDestroyView.as_view()),
    path("scheduleentry/", ScheduleEntryCreateView.as_view()),
]
