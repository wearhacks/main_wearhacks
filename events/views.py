from django.shortcuts import render
from django.forms.models import model_to_dict
from models import TeamMember,Event
from django.http import HttpResponse,JsonResponse
import datetime
import mailchimp
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
def current_datetime(request):
    now = datetime.datetime.now()
    html = "<html><body>It is now %s.</body></html>" % now
    return HttpResponse(html)

def home(request):
    return render(request, 'index.html')

def about_us(request):
    return render(request, 'aboutus.html',{'title':"About Us",'team_members':TeamMember.objects.all()})
def events(request):
    return render(request, 'events.html',{'title':"Events",'events':Event.objects.all().filter(start_date__gt = datetime.datetime.now()).order_by('start_date')})
def ambassador(request):
    return render(request, 'ambassador.html',{'title':"Ambassador Program"})


@csrf_exempt
def mailchimp_signup(request):
  if request.method == 'POST':
    try:
        m = mailchimp.Mailchimp(settings.MAILCHIMP_API_KEY)
        m.lists.subscribe(settings.MAILCHIMP_LIST_ID, {'email':request.POST['email']})
        return JsonResponse({"status":"success", "message":"The email has been successfully subscribed"})
    except mailchimp.ListAlreadySubscribedError:
        return JsonResponse({"status":"error", "message":"That email is already subscribed to the list"})
    except mailchimp.Error, e:
        return JsonResponse({"status":"error","message":'An error occurred: %s - %s' % (e.__class__, e)})
  else:
    return JsonResponse({"status":"error", "message":"There is no email"})
    

