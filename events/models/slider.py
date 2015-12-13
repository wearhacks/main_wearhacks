from django.db import models
from events.models.helpers import *

class Slider(models.Model):
    SLIDERTYPES = (
        ('0', 'MAIN PAGE'),
        ('1', 'MISSION PAGE'),
        ('2', 'AMBASSADOR PAGE')
    )
    
    name = models.CharField(max_length = 150)
    order = models.IntegerField(default=0)

    photo = models.ImageField(upload_to = get_upload_path, blank = True, null = True)
    
    main_text = models.TextField()
    first_link_text = models.CharField(max_length = 50, blank=True)
    first_link = models.CharField(max_length=100, blank=True)
    second_link_text = models.CharField(max_length = 50,  blank=True)
    second_link = models.CharField(max_length=100, blank=True)
    

    overlay_percentage = models.DecimalField(default=0.00, max_digits=2, decimal_places=2, blank=False, help_text="Specify background opacity 0~>1.  0 -> Clear image, 1-> completely dark")
    align_left = models.BooleanField(default=False)
    add_call_to_action = models.BooleanField(default=False)
    slider_location = models.CharField(max_length=1, choices=SLIDERTYPES, default = 0)