# This file is part of radiocontrol.
#
# Copyright (C) 2015 Stefan Derkits <stefan@derkits.at>
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

from bootstrap3_datetime.widgets import DateTimePicker

from django import forms
from django.utils import timezone
from django.forms import ValidationError

from datetime import datetime, timedelta

from control.models import Playlist, ScheduleEntry


class ScheduleEntryForm(forms.Form):
    playlist = forms.ModelChoiceField(queryset=Playlist.objects.all().order_by("name"), empty_label=None)
    nowstr = datetime.now().strftime("%d-%m-%Y %H:%M")
    print("nowstr: %s" % nowstr)
    begin_time = forms.DateTimeField(
        widget=DateTimePicker(options=dict(format="DD-MM-YYYY HH:mm", pickTime=True, stepping=15, sideBySide=True)),
        input_formats=['%d-%m-%Y %H:%M'])
