from django.db import models
from events.models.helpers import *
from django.core.files.images import get_image_dimensions
from django.core.exceptions import ValidationError

def validate_image(fieldfile_obj):
  filesize = fieldfile_obj.file.size
  megabyte_limit = 0.5
  if filesize > megabyte_limit*1024*1024:
    raise ValidationError("Max file size is %sMB" % str(megabyte_limit))
  w, h = get_image_dimensions(fieldfile_obj.file)
  if w > 500 or h > 500:
    raise ValidationError("The image is %i pixel wide. Max 500px * 500px " % w)
class Partner(models.Model):
    PARTNERTYPES = (
        ('0', 'Global Partners'),
        ('1', 'Hardware Partners'),
        ('2', 'Media Partners'),
        ('3', 'Ecosystem Partners'),
        ('4', 'Legal Partners'),
        ('5', 'Previous City Partners'),
    )

    def displayedType(self):
        return self.PARTNERTYPES[int(self.partner_type)][1]

    name = models.CharField(max_length = 50)
    partner_type = models.CharField(max_length=1, choices=PARTNERTYPES)
    photo = models.ImageField(upload_to = get_upload_path, blank = True, null = True,  validators=[validate_small_image])
    link = models.URLField(max_length=100, blank=True)
    short_description = models.CharField(max_length = 150)
    type = displayedType

    def __unicode__(self):
        return u"%s" % self.name

    class Meta:
        app_label = 'events'
