from django.shortcuts import render, redirect
from django.forms.models import model_to_dict
from django.core.mail import EmailMessage
from django.core.exceptions import ObjectDoesNotExist
from models import TeamMember, Event,PastEvent, Partner, Slider, Project, WorkshopInstance
from forms import PartnerForm
from django.http import HttpResponse,JsonResponse
from urllib import urlopen
import datetime
import mailchimp
import json
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from constance import config
import itertools as iTool
import random

def home(request):
    def get_random_projects(num_projects):
        """
        Get <num_projects> random projects to showcase on the homepage. 
        Might need to find another way to handle random selection as this method
         does not scale well.
        """
        projects = Project.objects.filter(project_type='2').order_by('?')[:num_projects]
        return projects

    events = Event.objects.all().filter(start_date__gt = datetime.datetime.now()).order_by('start_date')
    if len(events) > 0:
        event = events[0]
    else:
        event = None
    content = {
        'title' : "Home",
        'config':config,
        'blog_title' : '',
        'blog_excerpt' : '',
        'blog_link' : '',
        'blog_image' : '',
        'event' : event,
        'slides' : Slider.objects.filter(slider_location = 0).order_by('order'),
        'past_events': Event.objects.filter(pastevent__in = PastEvent.objects.all())
                                    .filter(start_date__lt = datetime.datetime.now())
                                    .order_by('-start_date')[:3],
        'random_projects': get_random_projects(4)
    }

    return render(request, 'index.html',content)

def team(request):
    return render(request, 'ourteam.html',
        {'title':"Our Team",
         'team_members':TeamMember.objects.all().order_by('name'),
         'config':config})

def workshop(request, workshop):
    workshop = WorkshopInstance.objects.get(slug = workshop)
    return render(request, 'workshop.html', {'config':config, 'workshop':workshop})
def events(request, event_slug=None):
    if (event_slug):
        try:
            event = Event.objects.get(slug = event_slug)
            response =  {
                'config':config,
                'title':event.event_name,
                'event':event,
                'stats':{}}
            past_event = event.pastevent
            if past_event:
                response['stats'] = past_event.get_stats()
                response['allPictures'] = past_event.fetch_photos()

            winning_projects = event.project_set.filter(project_type='2')
            projects = event.project_set.filter(project_type='1')
            
            all_proj = len(projects)+ len(winning_projects)
            if (len(winning_projects) <=3 or all_proj <= 10) :
                response['top_projects'] = event.project_set.all()
                response['bottom_projects'] = []
            else:
                response['top_projects'] = winning_projects
                response['bottom_projects'] = projects

            response['stats']['projects'] = all_proj
            response['stats']['winning'] = len(winning_projects)

            return render(request, 'event_pictures.html', response)
        except ObjectDoesNotExist:
            return redirect('events')
    return render(request, 'events.html',
        {'config':config,
         'title':"Events",
         'events':Event.objects.all().filter(start_date__gt = datetime.datetime.now()).order_by('start_date'),
         'past_events': Event.objects.all().filter(start_date__lt = datetime.datetime.now()).order_by('start_date'),
         'workshops': WorkshopInstance.objects.all().filter(start_date__gt = datetime.datetime.now()).order_by('start_date'),
         'config':config})
def projects(request) :
    return render(request, 'projects.html',
        {'config':config,
         'title':"Projects",
         'top_projects':Project.objects.filter(project_type='2'),
         'bottom_projects': Project.objects.filter(project_type='1'),
         'config':config})

def ambassador(request):
    return render(request, 'ambassador.html',{
      'slides' : Slider.objects.filter(slider_location = 2).order_by('order'),
      'config':config,
      'title':"Ambassador Program"})
def mission(request):
    return render(request, 'mission.html',{
        'slides' : Slider.objects.filter(slider_location = 1).order_by('order'),
        'config':config, 'title':"Our Mission"})


def partnerships(request):
    if request.method == 'POST':
        form = PartnerForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['organization_name'] + ' wants to be our partner!'
            message = form.cleaned_data['message']
            email = form.cleaned_data['email']
            recipients = ['info@wearhacks.com']

            EmailMessage(subject, message, email, recipients).send()
            return JsonResponse({"status":"success", "message":"Welcome aboard!<br>:)"}, status=200)
        else:
            return JsonResponse({"status":"failure", "message":"Please make sure that you entered a valid email."}, status=400)
    else :
        form = PartnerForm()
        partners = iTool.groupby(Partner.objects.all(), lambda x: int(x.partner_type)) # int() will order the type correctly

        return render(request, 'partnerships.html',
            {'title':"Partnerships",
             'partners':{k: list(v) for k, v in partners},
             'form': form,
             'config':config
            })

@csrf_exempt
def mailchimp_signup(request):
  if request.method == 'POST':
    try:
        m = mailchimp.Mailchimp(settings.MAILCHIMP_API_KEY)
        m.lists.subscribe(settings.MAILCHIMP_LIST_ID, {'email':request.POST['email']})
        return JsonResponse({"status":"success", "message":"The email has been successfully subscribed"}, status=200)
    except mailchimp.ListAlreadySubscribedError:
        return JsonResponse({"status":"error", "message":"That email is already subscribed to the list"}, status=400)
    except mailchimp.Error, e:
        return JsonResponse({"status":"error","message":'An error occurred: %s - %s' % (e.__class__, e)}, status=400)
  else:
    return JsonResponse({"status":"error", "message":"There is no email"}, status = 400)

def get_sticky_post(request):
    url = urlopen(config.A_BLOG_LINK + '/?json=1').read()
    print url
    return JsonResponse(json.loads(url))
