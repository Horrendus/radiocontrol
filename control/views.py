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

from django.shortcuts import render, render_to_response

from django.contrib.auth.decorators import login_required
from django.contrib import messages

from django.template import RequestContext

from django.core.exceptions import ValidationError

from django.contrib import auth
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse
from django.utils import timezone

from datetime import datetime

from control.forms import ScheduleEntryForm
from control.models import Playlist, ScheduleEntry


def index(request):
    if request.method == 'GET':
        return HttpResponse("TODO", content_type='text/plain')


@login_required()
def schedule(request):
    if request.method == 'GET':
        old = request.GET.get('old')
        if old:
            all_entries = ScheduleEntry.objects.all().order_by('begin_time')
        else:
            all_entries = (obj for obj in ScheduleEntry.objects.all() if obj.end_time >= timezone.now())
        return render_to_response('schedule.html', {'all_entries': all_entries, 'display_old': old}, context_instance=RequestContext(request))
    if request.method == 'POST':
        print(request.POST)
        form = ScheduleEntryForm(request.POST)
        if form.is_valid():
            entry = ScheduleEntry(**form.cleaned_data)
            try:
                entry.clean()
                entry.save()
                return HttpResponseRedirect('/schedule.html')
            except ValidationError as e:
                print("Model not valid")
                return HttpResponse(str(e), content_type='text/plain')
        else:
            print("Validty check failed")
            return HttpResponse(str(form.errors), content_type='text/html')




@login_required
def new_schedule(request):
    if request.method == 'GET':
        form = ScheduleEntryForm()
    else:
        form = ScheduleEntryForm(request.POST)
    return render(request, "new_schedule.html", dict(form=form))


def sessions(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)
        if user is not None and user.is_active:
            auth.login(request, user)
            next_url = request.POST.get('next','/')
            if len(next_url) is 0:
                return HttpResponseRedirect('/')
            else:
                return HttpResponseRedirect(next_url)

        else:
            messages.error( request, 'Could not log in' )
            return HttpResponseRedirect("/")


def destroy_session(request):
    auth.logout(request)
    return HttpResponseRedirect("/")
