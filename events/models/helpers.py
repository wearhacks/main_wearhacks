import os
import re
from django.core.files.images import get_image_dimensions
from django.core.exceptions import ValidationError
 
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

def get_upload_path_project(instance, filename):
    folder = 'projects'
    new_filename = re.sub('[^a-zA-Z0-9]', '', instance.project_name) + '_' + filename
    return os.path.join(folder, new_filename)

def validate_large_image(fieldfile_obj):
    filesize = fieldfile_obj.file.size
    megabyte_limit = 1.0
    if filesize > megabyte_limit*1024*1024:
      raise ValidationError("Max file size is %sMB" % str(megabyte_limit))
    w, h = get_image_dimensions(fieldfile_obj.file)
    if w > 2000 or h > 2000:
      raise ValidationError("The image is %i pixel wide. Max 2000px * 2000px " % w)

def validate_small_image(fieldfile_obj):
  filesize = fieldfile_obj.file.size
  megabyte_limit = 0.5
  if filesize > megabyte_limit*1024*1024:
    raise ValidationError("Max file size is %sMB" % str(megabyte_limit))
  w, h = get_image_dimensions(fieldfile_obj.file)
  if w > 500 or h > 500:
    raise ValidationError("The image is %i pixel wide. Max 500px * 500px " % w)