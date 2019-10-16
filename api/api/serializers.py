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
        fields = ("name", "entries")

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


# TODO: this needs a complete rewrite, best to start from scratch
"""
class ScheduleEntrySerializer(serializers.ModelSerializer):
    playlists = serializers.SlugRelatedField(many=True, slug_field='name', queryset=Playlist.objects.all())

    class Meta:
        model = ScheduleEntry
        fields = ('begin_datetime', 'playlists')
        extra_kwargs = {
            'playlists': {
                'validators': [],
            }
        }

    def create(self, validated_data):
        begin_datetime = validated_data.pop('begin_datetime')
        playlists = validated_data.pop('playlists')
        schedule_entry = ScheduleEntry.objects.create(begin_datetime=begin_datetime)
        for playlist in playlists:
            ScheduleEntryOrder.objects.create(schedule_entry=schedule_entry, playlist=playlist)
        return schedule_entry

    def update(self, instance, validated_data):
        print("update not implemented yet")
        return instance

    def validate(self, data):
        begin_datetime = data['begin_datetime']
        duration = sum([p.length for p in data["playlists"]])
        closest_schedule_entries = ScheduleEntry.get_closest_to(begin_datetime)
        for playlist in data["playlists"]:
            if playlist.status == PlaylistEntryStatus.ERROR:
                raise ValidationError(f"Can not schedule playlist {playlist.name} because of errors.")
        if closest_schedule_entries["before"]:
            entry_before = closest_schedule_entries["before"]
            end_of_before = entry_before.begin_datetime + timedelta(seconds=entry_before.length)
            if end_of_before > begin_datetime:
                raise ValidationError("ScheduleEntry must begin after end of last ScheduleEntry")
        if closest_schedule_entries["after"]:
            entry_after = closest_schedule_entries["after"]
            end_of_current = begin_datetime + timedelta(seconds=duration)
            begin_of_next = entry_after.begin_datetime
            if end_of_current > begin_of_next:
                raise ValidationError("ScheduleEntry must end before begin of next ScheduleEntry")
        return data
"""
