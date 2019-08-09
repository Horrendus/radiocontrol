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

import json

from importlib import import_module

from django.views import View
from django.http import HttpResponse
from django.conf import settings

from rest_framework import generics

from api.models import Song, Playlist, ScheduleEntry, PlaylistEntry
from api.serializers import PlaylistEntrySerializer, PlaylistSerializer, ScheduleEntrySerializer

media_backend = import_module(settings.MEDIA_BACKEND)


class SongListView(generics.ListAPIView):
    queryset = Song.objects.all()
    serializer_class = PlaylistEntrySerializer


class PlaylistListView(generics.ListCreateAPIView):
    queryset = Playlist.objects.all()
    serializer_class = PlaylistSerializer


class PlaylistReadUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Playlist.objects.all()
    serializer_class = PlaylistSerializer
    lookup_field = 'name'


class ScheduleEntryListView(generics.ListCreateAPIView):
    queryset = ScheduleEntry.objects.all()
    serializer_class = ScheduleEntrySerializer


class ScheduleEntryReadUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ScheduleEntry.objects.all()
    serializer_class = ScheduleEntrySerializer
    lookup_field = 'begin_time'


class MediaCreateView(View):

    http_method_names = ['post', 'head', 'options', 'trace']

    @staticmethod
    def post(request):
        mediadata = json.loads(request.body)
        valid = list()
        valid.append('artist' in mediadata)
        valid.append('title' in mediadata)
        valid.append('filename' in mediadata)
        valid.append('data' in mediadata)
        if all(valid):
            save_ok = media_backend.save_media(mediadata)
            if save_ok:
                Song.objects.create(**mediadata)
                playlist_entries = PlaylistEntry.objects.filter(filename=mediadata["filename"])
                for playlist_entry in playlist_entries:
                    playlist_entry.update_status()
                return HttpResponse(status=201)


class MediaReadUpdateDestroyView(View):

    http_method_names = ['get', 'put', 'delete', 'head', 'options', 'trace']

    def get(self, request, *args, **kwargs):
        pass

    def put(self, request, *args, **kwargs):
        pass

    def delete(self, request, *args, **kwargs):
        pass
