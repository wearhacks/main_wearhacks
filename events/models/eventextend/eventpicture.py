from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from events.models.helpers import *

# Allow us to as a much pictures as we want per event
class EventPicture(models.Model):
	photo = models.ImageField(upload_to = get_upload_path_event_picture)
	event = models.ForeignKey('Event', on_delete=models.CASCADE)

	def __unicode__(self):
		return u"%s" % self.photo

	class Meta:
		app_label = 'events'