from django.db import models
from events.models.helpers import *
from geoposition.fields import GeopositionField

class Event(models.Model):
    EVENTTYPES = (
        ('workshop', 'Workshop'),
        ('alpha_hack', 'Alpha Hack'),
        ('hackathon', 'Hackathon')
    )

    """(Place description)"""
    def date_to_string(self):
        if self.start_date.year != self.end_date.year:
            return self.start_date.strftime('%d %b %Y') + '-' + self.end_date.strftime('%d %b %Y')
        elif self.start_date.month != self.end_date.month:
            return self.start_date.strftime('%d %b ') + ' to ' + self.end_date.strftime('%d %b %Y')
        else:
            return self.start_date.strftime('%d') + '-' + self.end_date.strftime('%d %b %Y')

    def get_long_extensions(self):
        return self.eventextend_set.select_related().filter(extendKey__icon__isnull=True).order_by('extendKey__priority')

    def get_iconable_extensions(self):
        return self.eventextend_set.select_related().filter(extendKey__icon__isnull=False).order_by('extendKey__priority')

    event_name = models.CharField(max_length = 50)
    slug = models.SlugField(blank=False,
         help_text="ie: Short name, required field for event page: http://wearhacks.com/events/<slug>")
    start_date = models.DateTimeField(blank=True)
    end_date = models.DateTimeField(blank=True, )
    address = models.CharField(max_length = 100)
    city = models.CharField(max_length= 50)
    photo = models.ImageField(upload_to = get_upload_path_event, blank = True, null = True, validators=[validate_large_image])
    location = GeopositionField()
    link = models.URLField(max_length=100, blank=True)
    date = date_to_string
    event_type = models.CharField(max_length=10, choices=EVENTTYPES, default='hackathon')
    registration_closed = models.BooleanField(default=False)
    long_extensions = get_long_extensions # note that front-end for displaying this is not implemented
    iconable_extensions = get_iconable_extensions

    def __unicode__(self):
        return u"%s" % self.event_name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify('%s %d' % (self.city, self.start_date.year))
        super(Event, self).save(*args, **kwargs)



    class Meta:
        app_label = 'events'