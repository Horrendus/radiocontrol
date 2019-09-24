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
from rest_framework import mixins

from api.models import Song, Playlist, ScheduleEntry, PlaylistEntry
from api.serializers import PlaylistEntrySerializer, PlaylistSerializer, ScheduleEntrySerializer

media_backend = import_module(settings.MEDIA_BACKEND)


class SongListView(generics.ListAPIView):
    queryset = Song.objects.all()
    serializer_class = PlaylistEntrySerializer


class PlaylistListCreateView(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = Playlist.objects.all()
    serializer_class = PlaylistSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):

        if "playlist" in request.FILES:
            playlist_file = request.FILES['playlist']
            print("file found: ", playlist_file)
            save_ok = media_backend.save_playlist(playlist_file)
            if save_ok:
                return HttpResponse(status=201)
            return HttpResponse("Error: Could not save playlist", status=500)
        else:
            return self.create(request, *args, **kwargs)


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

    http_method_names = ['post']

    @staticmethod
    def post(request):
        if "data" in request.FILES:
            save_ok = media_backend.save_media(request.FILES["data"])
            if save_ok:
                return HttpResponse(status=201)
            return HttpResponse("Error: Could not save file", status=500)
        else:
            return HttpResponse("Error: Media upload needs filename & file data", status=500)


class MediaReadUpdateDestroyView(View):

    http_method_names = ['get', 'put', 'delete']

    def get(self, request, *args, **kwargs):
        pass

    def put(self, request, *args, **kwargs):
        pass

    def delete(self, request, *args, **kwargs):
        pass
