from django.shortcuts import render
from django.forms.models import model_to_dict
from django.core.mail import EmailMessage
from models import TeamMember,Event,Partner
from forms import PartnerForm
from django.http import HttpResponse,JsonResponse
from urllib import urlopen
import datetime
import mailchimp
import json
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from constance import config
import itertools as iTool

def home(request):
    posts = json.loads(urlopen(config.A_BLOG_LINK + '/?json=1').read())["posts"]
    content = {
        'title' : "Home",
        'config':config,
        'blog_title' : posts[0]["title"], 
        'blog_excerpt' : posts[0]["excerpt"],
        'blog_link' : posts[0]["url"],
        'blog_image' : posts[0]["thumbnail_images"]["full"]["url"]
    }


    return render(request, 'index.html',content)

def about_us(request):
    return render(request, 'aboutus.html',
        {'title':"About Us",
         'team_members':TeamMember.objects.all().order_by('order'),
         'config':config})
def events(request):
    return render(request, 'events.html',{'config':config, 'title':"Events",'events':Event.objects.all().order_by('start_date'),'config':config})
def ambassador(request):
    return render(request, 'ambassador.html',{'config':config, 'title':"Ambassador Program"})

def partnerships(request):
    if request.method == 'POST':
        form = PartnerForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['organization_name'] + ' wants to be our partner!'
            message = form.cleaned_data['message']
            email = form.cleaned_data['email']

            recipients = ['i.nadim@gmail.com']

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
             'form': form
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
