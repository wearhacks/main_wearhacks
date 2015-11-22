from django.db import models
from django.contrib.auth.models import User
from geoposition.fields import GeopositionField
from django.template.defaultfilters import slugify
import flickrapi
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
    slug = models.SlugField(blank=True)
    def __unicode__(self):
        return u"%s" % self.short_name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify('%s %d' % (self.city, self.start_date.year))
        super(Event, self).save(*args, **kwargs)

class Project(models.Model):
    PROJECTTYPE = (
        ('0','staff'),
        ('1','participant'),
        ('2','winner')
    )

    submitted_event = models.ForeignKey(Event, blank=True)
    project_name = models.CharField(max_length = 50)
    short_description = models.CharField(max_length = 150)
    url = models.URLField(max_length=100, blank=True)
    image = models.URLField(max_length=100, blank=True)
    project_type = models.CharField(max_length=1, choices=PROJECTTYPE)

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
    album = None
    photos = None
    user = None

    def __unicode__(self):
        return u"%s : %s" % (self.source_albumname, self.event)

    def fetchAlbum(self):
        if not self.album:
            if self.source_type == '1': # if from flickr
                api_key = 'e889aef0eee347e6be9e6aa30da11cd5'
                api_secret = '633a019eba067bba'
                flickr = flickrapi.FlickrAPI(api_key, api_secret, format='parsed-json')
                sets = flickr.photosets.getPhotos(
                            user_id=self.source_username,
                            photoset_id=self.source_albumname)
                self.album = sets
            # handle other cases
        return self.album

    def fetchPhotos(self):
        if not self.photos:
            if not self.album:
                self.fetchAlbum()
            if self.source_type == '1': # if from flickr
                self.photos = self.album['photoset']['photo']
            # handle other cases
        return self.photos


