from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from events.models.helpers import *


class TeamMember(models.Model):

    name = models.CharField(max_length = 50)
    position = models.CharField(max_length = 50)
    blurb = models.CharField(max_length = 150)
    email = models.EmailField(verbose_name='email')
    photo = models.ImageField(upload_to = get_upload_path, blank = True, null = True,validators=[validate_small_image])
    github = models.URLField(max_length=100, blank=True)
    linkedin = models.URLField(max_length=100, blank=True)
    facebook = models.URLField(max_length=100, blank=True)
    twitter = models.URLField(max_length=100, blank=True)
    order = models.DecimalField(max_digits=100, decimal_places=0, default=0)

    def __unicode__(self):
        return u"%s" % self.name
    class Meta:
        verbose_name_plural = "Team Members"

    class Meta:
        app_label = 'events'
