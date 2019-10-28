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

import datetime

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
    end_datetime = serializers.ReadOnlyField()

    class Meta:
        model = ScheduleEntry
        fields = ("playlist", "begin_datetime", "end_datetime")

    @staticmethod
    def validate_playlist(playlist):
        print(f"validating playlist")
        if playlist.status == "PlaylistEntryStatus.ERROR":
            raise serializers.ValidationError("Can not schedule a playlist with errors")
        return playlist

    @staticmethod
    def validate_begin_datetime(begin_datetime):
        print(f"validating datetime {begin_datetime}")
        is_future = begin_datetime > (
            datetime.datetime.utcnow() + datetime.timedelta(minutes=5)
        )
        if not is_future:
            raise serializers.ValidationError(
                "begin_datetime not in the future (ts > now + 5min)"
            )
        return begin_datetime

    def validate(self, attrs):
        print("object level validation")
        print(f"attrs: {attrs}")
        playlist = attrs["playlist"]
        begin_datetime = attrs["begin_datetime"]
        closest_schedule_entries = ScheduleEntry.get_closest_to(begin_datetime)
        print(f"Closest: {closest_schedule_entries}")
        end_datetime = begin_datetime + datetime.timedelta(seconds=int(playlist.length))
        print(f"calculated playlist time: {begin_datetime} till {end_datetime}")
        if begin_datetime < closest_schedule_entries["before"].end_datetime:
            raise serializers.ValidationError(
                "Can not schedule: begin_time before the end of the previous schedule entry"
            )
        if end_datetime < closest_schedule_entries["after"].begin_datetime:
            raise serializers.ValidationError(
                "Can not schedule: end_time before the end of the next schedule entry"
            )
        return attrs
