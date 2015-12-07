from django.db import models
from event import Event

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

    class Meta:
        app_label = 'events'