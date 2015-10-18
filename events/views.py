from django.shortcuts import render
from django.forms.models import model_to_dict
from models import TeamMember,Event

from django.http import HttpResponse
import datetime

def current_datetime(request):
    now = datetime.datetime.now()
    html = "<html><body>It is now %s.</body></html>" % now
    return HttpResponse(html)

def home(request):
    return render(request, 'index.html')

def about_us(request):
    return render(request, 'aboutus.html',{'title':"About Us",'team_members':TeamMember.objects.all()})
def events(request):
    return render(request, 'events.html',{'title':"Events",'events':Event.objects.all()})