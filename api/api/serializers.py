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

from rest_framework import serializers

from api.models import Playlist, PlaylistOrder, PlaylistEntry, ScheduleEntry, Song


class PlaylistEntrySerializer(serializers.ModelSerializer):
    status = serializers.Field

    class Meta:
        model = PlaylistEntry
        fields = ("artist", "title", "filename", "length", "status")


class SongSerializer(serializers.ModelSerializer):
    class Meta:
        model = Song
        fields = ("artist", "title", "filename", "length")


class PlaylistSerializer(serializers.ModelSerializer):
    entries = PlaylistEntrySerializer(many=True)

    class Meta:
        model = Playlist
        fields = ("name", "entries", "status", "length")

    def create(self, validated_data):
        name = validated_data.pop("name")
        entries_data = validated_data.pop("entries")
        playlist = Playlist.objects.create(name=name)
        for entry_data in entries_data:
            entry, created = PlaylistEntry.objects.get_or_create(**entry_data)
            PlaylistOrder.objects.create(playlist=playlist, entry=entry)
        return playlist

    def update(self, instance, validated_data):
        print("update not implemented yet")
        return instance


class ScheduleEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = ScheduleEntry
        fields = ("begin_datetime", "playlist")
