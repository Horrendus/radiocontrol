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

import base64
import os
import json
from importlib import import_module

from rest_framework.exceptions import APIException

from django.test import TestCase
from django.test import Client
from django.conf import settings


class FileMediaBackendTest(TestCase):
    def setUp(self):
        self.backend = import_module("api.file_mediabackend")
        self.backend.MEDIA_ROOT = "/tmp/file_media_test/"
        self.testdata_path = os.path.dirname(os.path.abspath(__file__)) + "/testdata/"
        self.client = Client()
        # allow client
        settings.ALLOWED_HOSTS.append("testserver")

    def test_upload(self):
        file1_filename = "Scott_Holmes_-_Happy_Days.mp3"
        file1_name = self.testdata_path + file1_filename
        with open(file1_name, "rb") as f:
            file1_data_b64 = base64.b64encode(f.read())
        file1_metadata = {
            "artist": "Scott Holmes",
            "title": "Happy Days",
            "filename": file1_filename,
            "data": str(file1_data_b64, "UTF-8"),
        }
        file1_json = json.dumps(file1_metadata)
        self.client.post("/media/", file1_json, content_type="application/json")

    def test_m3u_entry_parse_tooshort(self):
        line = "#EXTIN"
        with self.assertRaises(APIException) as e:
            self.backend.parse_m3u_playlist_entry(line)
        self.assertEqual(e.exception.detail, "invalid extinf line: too short")

    def test_m3u_entry_parse_nolengthseperator(self):
        line = "#EXTINF:300"
        with self.assertRaises(APIException) as e:
            self.backend.parse_m3u_playlist_entry(line)
        self.assertEqual(
            e.exception.detail, "invalid extinf line: no length seperator found"
        )

    def test_m3u_entry_parse_lengthnoint(self):
        line = "#EXTINF:ABC,"
        with self.assertRaises(APIException) as e:
            self.backend.parse_m3u_playlist_entry(line)
        self.assertEqual(
            e.exception.detail, "invalid extinf line: length not an integer"
        )

    def test_m3u_entry_parse_noartistseperator(self):
        line = "#EXTINF:300,Artist_Title"
        with self.assertRaises(APIException) as e:
            self.backend.parse_m3u_playlist_entry(line)
        self.assertEqual(
            e.exception.detail, "invalid extinf line: no artist seperator found"
        )

    def test_m3u_entry_parse_notitle(self):
        line = "#EXTINF:300,Artist -"
        with self.assertRaises(APIException) as e:
            self.backend.parse_m3u_playlist_entry(line)
        self.assertEqual(
            e.exception.detail, "invalid extinf line: tag doesnt have title"
        )

    def test_m3u_entry_parse_emptytitle(self):
        line = "#EXTINF:300,Artist -    "
        with self.assertRaises(APIException) as e:
            self.backend.parse_m3u_playlist_entry(line)
        self.assertEqual(
            e.exception.detail, "invalid extinf line: artist or title empty"
        )

    def test_m3u_entry_parse_emptyartist(self):
        line = "#EXTINF:300,     -    Title"
        with self.assertRaises(APIException) as e:
            self.backend.parse_m3u_playlist_entry(line)
        self.assertEqual(
            e.exception.detail, "invalid extinf line: artist or title empty"
        )
