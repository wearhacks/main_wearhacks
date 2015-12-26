from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from ..models import Event
from registration.forms import WorkshopRegistrationForm
from django.http import HttpResponse,JsonResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import datetime
from constance import config
import itertools as iTool

def workshops(request, event_slug=None):
    if (event_slug):
        try:
            event = Event.objects.get(slug = event_slug)
            response =  {
                'config':config,
                'title':event.event_name,
                'event':event,
                'stats':{}}
            if event.event_type == 'workshop':
                response['contents'] = event.eventcontent_set.all().order_by('priority').filter(draft=False)
                response['tickets'] = event.ticket_set.all().order_by('priority')
                response['form'] = WorkshopRegistrationForm(response['tickets'])
                return render(request, 'workshop_detail.html', response)
            elif event.event_type == 'hackathon':
                return redirect('events/'+event_slug)
        except ObjectDoesNotExist:
            return redirect('workshops')

    allEvents = Event.objects.all().filter(event_type='workshop')
    return render(request, 'workshops.html',
        {'config':config,
         'title':"Workshops",
         'events':allEvents.filter(start_date__gt=datetime.datetime.now()).order_by('start_date'),
         'past_events': allEvents.filter(start_date__lt=datetime.datetime.now()).order_by('start_date'),
         'config':config})
