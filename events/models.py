from django.db import models
from django.contrib.auth.models import User
from geoposition.fields import GeopositionField
import os

def get_image_path(instance, filename):
    return os.path.join('', str(instance.id), filename)

def get_event_img_path(instance,filename):
    return os.path.join('events', str(instance.id), filename)

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
    photo = models.ImageField(upload_to = get_event_img_path, blank = True, null = True)
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
    photo = models.ImageField(upload_to = get_image_path, blank = True, null = True)
    github = models.URLField(max_length=100, blank=True)
    linkedin = models.URLField(max_length=100, blank=True)
    facebook = models.URLField(max_length=100, blank=True)
    twitter = models.URLField(max_length=100, blank=True)

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
    photo = models.ImageField(upload_to = get_event_img_path, blank = True, null = True)
    link = models.URLField(max_length=100, blank=True)
    type = displayedType

    def __unicode__(self):
        return u"%s" % self.name


class Content(models.Model):
    name = models.CharField(max_length = 50) # name indentifier for queries
    sub_name = models.CharField(max_length = 50, blank=True) # same as above, but unique
    # e.g. if we have a group of texts with the same properties, this can be useful

    page_name = models.CharField(max_length = 50) # name of the template (use this in the views)

    title = models.CharField(max_length = 100, blank=True) # displayed title in the template
    content = models.CharField(max_length = 8000) # displayed content in the template

    def __unicode__(self):
        return u"%s" % self.content