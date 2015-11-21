from django.db import models
from django.contrib.auth.models import User
from geoposition.fields import GeopositionField
import flickr_api
from django.core.cache import cache
import os
import re

def get_upload_path(instance, filename):
    folder = type(instance).__name__.lower()
    new_filename = re.sub('[^a-zA-Z0-9]', '', instance.name) + os.path.splitext(filename)[1]
    return os.path.join(folder, new_filename)

def get_upload_path_event(instance, filename):
    folder = type(instance).__name__.lower()
    new_filename = re.sub('[^a-zA-Z0-9]', '', instance.event_name) + os.path.splitext(filename)[1]
    return os.path.join(folder, new_filename)

def get_upload_path_partner(instance, filename):
    folder = type(instance).__name__.lower()
    new_filename = re.sub('[^a-zA-Z0-9]', '', instance.name) + os.path.splitext(filename)[1]
    return os.path.join(folder, new_filename)

class Event(models.Model):
    """(Place description)"""
    def date_to_string(self):
        if self.start_date.year != self.end_date.year:
            return self.start_date.strftime('%d %b %Y') + '-' + self.end_date.strftime('%d %b %Y')
        elif self.start_date.month != self.end_date.month:
            return self.start_date.strftime('%d %b ') + ' to ' + self.end_date.strftime('%d %b %Y')
        else:
            return self.start_date.strftime('%d') + '-' + self.end_date.strftime('%d %b %Y')

    event_name = models.CharField(max_length = 50)
    short_name = models.CharField(max_length = 50)
    start_date = models.DateTimeField(blank=True)
    end_date = models.DateTimeField(blank=True, )
    address = models.CharField(max_length = 100)
    city = models.CharField(max_length= 50)
    photo = models.ImageField(upload_to = get_upload_path_event, blank = True, null = True)
    location = GeopositionField()
    link = models.URLField(max_length=100, blank=True)
    date = date_to_string
    def __unicode__(self):
        return u"%s" % self.short_name

class Project(models.Model):
    """(Place description)"""
    submitted_event = models.ForeignKey (Event)
    project_name = models.CharField(max_length = 50)
    short_description = models.CharField(max_length = 150)
    blog_post = models.URLField(max_length=100, blank=True)

    def __unicode__(self):
        return u"%s from %s " % (self.project_name, self.submitted_event.short_name)
class TeamMember(models.Model):

    name = models.CharField(max_length = 50)
    position = models.CharField(max_length = 50)
    blurb = models.CharField(max_length = 150)
    email = models.EmailField(verbose_name='email')
    photo = models.ImageField(upload_to = get_upload_path, blank = True, null = True)
    github = models.URLField(max_length=100, blank=True)
    linkedin = models.URLField(max_length=100, blank=True)
    facebook = models.URLField(max_length=100, blank=True)
    twitter = models.URLField(max_length=100, blank=True)
    order = models.DecimalField(max_digits=100, decimal_places=0, default=0)

    def __unicode__(self):
        return u"%s" % self.name
    class Meta:
        verbose_name_plural = "Team Members"

class Partner(models.Model):
    PARTNERTYPES = (
        ('0', 'Global Partners'),
        ('1', 'Hardware Partners'),
        ('2', 'Media Partners'),
        ('3', 'Membership'),
    )
    def displayedType(self):
        return self.PARTNERTYPES[int(self.partner_type)][1]

    name = models.CharField(max_length = 50)
    partner_type = models.CharField(max_length=1, choices=PARTNERTYPES)
    photo = models.ImageField(upload_to = get_upload_path, blank = True, null = True)
    link = models.URLField(max_length=100, blank=True)
    short_description = models.CharField(max_length = 150)
    type = displayedType

    def __unicode__(self):
        return u"%s" % self.name


class EventPicture(models.Model):
    SOURCETYPES = (
        ('0', 'Other'), # later we can add more sources
        ('1', 'flickr')
    )

    source_username = models.CharField(max_length = 50)
    source_albumname = models.CharField(max_length = 50)
    source_type = models.CharField(max_length=1, choices=SOURCETYPES)
    event = models.ForeignKey(Event)

    def __unicode__(self):
        return u"%s : %s" % (self.source_albumname, self.event)

    def fetchPictures(self):
        if self.source_type == '1': # if from flickr
            flickr_api.set_keys(# keys
                api_key = 'e889aef0eee347e6be9e6aa30da11cd5',
                api_secret = '633a019eba067bba')
            flickr_api.enable_cache(cache)
            user = flickr_api.Person.findByUserName(self.source_username)
            photosets = user.getPhotosets()
            return photoset.getPhotos()

        return None