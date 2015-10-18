from django.db import models
from django.contrib.auth.models import User
from geoposition.fields import GeopositionField



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
    end_date = models.DateTimeField(blank=True)
    address = models.CharField(max_length = 100)
    city = models.CharField(max_length= 50)
    location = GeopositionField()
    link = models.URLField(max_length=100, blank=True)
    date = date_to_string


class Projects(models.Model):
    """(Place description)"""
    submitted_by = models.ForeignKey (User)
    project_name = models.CharField(max_length = 50)

class TeamMember(models.Model):
    name = models.CharField(max_length = 50)
    position = models.CharField(max_length = 50)
    blurb = models.CharField(max_length = 150)
    email = models.EmailField(verbose_name='email')
    github = models.URLField(max_length=100, blank=True)
    linkedin = models.URLField(max_length=100, blank=True)
    facebook = models.URLField(max_length=100, blank=True)
    twitter = models.URLField(max_length=100, blank=True)
    def __unicode__(self):
        return u"%s" % self.name
    class Meta:
        verbose_name_plural = "Team Members"