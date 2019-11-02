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

from importlib import import_module

from django.views import View

from rest_framework import generics
from rest_framework import mixins
from rest_framework import response
from rest_framework import status

from api.models import Song, Playlist, ScheduleEntry
from api.serializers import PlaylistSerializer, ScheduleEntrySerializer, SongSerializer
from api import file_mediabackend as media_backend


class SongListView(generics.ListAPIView):
    queryset = Song.objects.all()
    serializer_class = SongSerializer


class PlaylistListCreateView(mixins.ListModelMixin, generics.GenericAPIView):
    queryset = Playlist.objects.all()
    serializer_class = PlaylistSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    @staticmethod
    def post(request, *args, **kwargs):

        if "playlist" in request.FILES:
            playlist_file = request.FILES["playlist"]
            print("file found: ", playlist_file)
            media_backend.save_playlist(playlist_file)
            return response.Response(
                {"success": "true"}, status=status.HTTP_201_CREATED
            )
        else:
            return response.Response(
                {"success": "false"}, status=status.HTTP_400_BAD_REQUEST
            )


class PlaylistReadUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Playlist.objects.all()
    serializer_class = PlaylistSerializer
    lookup_field = "name"


class ScheduleEntryListView(generics.ListCreateAPIView):
    queryset = ScheduleEntry.objects.all()
    serializer_class = ScheduleEntrySerializer


class ScheduleEntryCreateView(generics.CreateAPIView):
    queryset = ScheduleEntry.objects.all()
    serializer_class = ScheduleEntrySerializer


class ScheduleEntryReadDestroyView(generics.RetrieveDestroyAPIView):
    queryset = ScheduleEntry.objects.all()


class MediaCreateView(View):

    http_method_names = ["post"]

    @staticmethod
    def post(request):
        if "data" in request.FILES:
            save_ok = media_backend.save_media(request.FILES["data"])
            if save_ok:
                return response.Response(
                    {"success": "true"}, status=status.HTTP_201_CREATED
                )
            return response.Response(
                {"success": "false"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        else:
            return response.Response(
                {"success": "false"}, status=status.HTTP_400_BAD_REQUEST
            )


class MediaReadUpdateDestroyView(View):

    http_method_names = ["get", "put", "delete"]

    def get(self, request, *args, **kwargs):
        pass

    def put(self, request, *args, **kwargs):
        pass

    def delete(self, request, *args, **kwargs):
        pass
