from django.shortcuts import render
from django.http import HttpResponse
from django.template import Context, loader

def error404(request):
    return render(request,'errors/404.html')

def error500(request):
    return render(request,'errors/500.html')