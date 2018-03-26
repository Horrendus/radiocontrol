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
from rest_framework.validators import ValidationError

from datetime import timedelta

from api.models import DraftSong, DraftPlaylist, DraftPlaylistOrder, Song, Playlist, PlaylistOrder, ScheduleEntry, \
    ScheduleEntryOrder
from api.validators import ExistsValidator


class DraftSongSerializer(serializers.ModelSerializer):
    class Meta:
        model = DraftSong
        fields = ('artist', 'name', 'filename', 'length')
        extra_kwargs = {
            'filename': {
                'validators': [],
            }
        }


class DraftPlaylistSerializer(serializers.ModelSerializer):
    songs = DraftSongSerializer(many=True)

    class Meta:
        model = DraftPlaylist
        fields = ('name', 'songs')

    def create(self, validated_data):
        name = validated_data.pop('name')
        songs_data = validated_data.pop('songs')
        playlist = DraftPlaylist.objects.create(name=name)
        for song_data in songs_data:
            song, created = DraftSong.objects.get_or_create(**song_data)
            print(song, created)
            DraftPlaylistOrder.objects.create(playlist=playlist, song=song)
        return playlist

    def update(self, instance, validated_data):
        print("update not implemented yet")
        return instance


class SongSerializer(serializers.ModelSerializer):
    class Meta:
        model = Song
        fields = ('artist', 'name', 'filename')
        extra_kwargs = {
            'filename': {
                'validators': [ExistsValidator(queryset=Song.objects.all())],
            }
        }


class PlaylistSerializer(serializers.ModelSerializer):
    songs = SongSerializer(many=True)

    class Meta:
        model = Playlist
        fields = ('name', 'songs')

    def create(self, validated_data):
        name = validated_data.pop('name')
        songs_data = validated_data.pop('songs')
        playlist = Playlist.objects.create(name=name)
        for song_data in songs_data:
            song = Song.objects.get(filename=song_data["filename"])
            print(song)
            PlaylistOrder.objects.create(playlist=playlist, song=song)
        return playlist

    def update(self, instance, validated_data):
        print("update not implemented yet")
        return instance


class PlaylistNameSerializer(serializers.ModelSerializer):

    class Meta:
        model = Playlist
        fields = ['name']
        extra_kwargs = {
            'name': {
                'validators': [ExistsValidator(queryset=Playlist.objects.all())],
            }
        }


class ScheduleEntrySerializer(serializers.ModelSerializer):
    playlists = PlaylistNameSerializer(many=True)

    class Meta:
        model = ScheduleEntry
        fields = ('begin_datetime', 'playlists')

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
        playlists_data = data.pop('playlists')
        begin_datetime = data['begin_datetime']
        playlists = []
        for playlist_data in playlists_data:
            playlist_name = playlist_data['name']
            playlist = Playlist.objects.get(name=playlist_name)
            playlists.append(playlist)
        duration = sum([p.length for p in playlists])
        closest_schedule_entries = ScheduleEntry.get_closest_to(begin_datetime)
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
        data["playlists"] = playlists
        return data
