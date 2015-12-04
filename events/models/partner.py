from django.db import models
from events.models.helpers import *

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

    class Meta:
        app_label = 'events'
