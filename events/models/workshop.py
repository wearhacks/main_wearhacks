from django.db import models
from events.models.helpers import *
from geoposition.fields import GeopositionField


class Workshop(models.Model):
    DIFFICULTY = (
        ('0', 'Beginner'),
        ('1', 'Intermediate'),
        ('2', 'Advanced')
    )

    name = models.CharField(max_length = 150)
    short_description = models.CharField(max_length = 150)

    photo = models.ImageField(upload_to = get_upload_path, blank = True, null = True, validators=[validate_large_image])
    difficulty = models.CharField(max_length=1, choices=DIFFICULTY)
    required_tools = models.CharField(max_length=150)
    technologies = models.CharField(max_length=150, blank=False,
         help_text="Software or hardware technologies thought in this workshop")
    duration = models.CharField(max_length=150, blank=False,
         help_text="Approximate duration of the course")
    schedule = models.TextField(default='<ul><li><span>9:00AM</span> Quick Introduction</li><li><span>-:--AM</span> etc </li></ul>')
    workshop_outline = models.TextField(default='<h1>What is this workshop about?</h1> <p>Describe event<p>')

    def difficulty_text(self): 
        return self.DIFFICULTY[int(self.difficulty)][1]

class WorkshopInstance(models.Model):
    def date_to_string(self):
        if self.start_date.year != self.end_date.year:
            return self.start_date.strftime('%d %b %Y') + '-' + self.end_date.strftime('%d %b %Y')
        elif self.start_date.month != self.end_date.month:
            return self.start_date.strftime('%d %b ') + ' to ' + self.end_date.strftime('%d %b %Y')
        elif self.start_date.day != self.end_date.day:
            return self.start_date.strftime('%d') + '-' + self.end_date.strftime('%d %b %Y')
        else:
            return self.start_date.strftime('%H:%M') + ' to ' + self.end_date.strftime('%H:%M') + ' on ' + self.end_date.strftime('%b %d, %Y')

    parent_workshop = models.ForeignKey(Workshop, blank=True)
    start_date = models.DateTimeField(blank=True)
    end_date = models.DateTimeField(blank=True)

    eventbrite_link = models.URLField(blank=False)
    slug = models.SlugField(blank=False,
         help_text="ie: Short name, required field for event page: http://wearhacks.com/workshops/<slug>")
    address = models.CharField(max_length = 100)
    location = GeopositionField()
    date = date_to_string
    

class WorkshopTutor(models.Model):
    workshop = models.ForeignKey(WorkshopInstance, blank=True)
    name = models.CharField(max_length = 50)
    title = models.CharField(max_length = 150)
    email = models.EmailField(verbose_name='email')
    photo = models.ImageField(upload_to = get_upload_path, blank = True, null = True,validators=[validate_small_image])
    background = models.TextField(max_length=150)
