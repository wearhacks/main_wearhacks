from django.contrib import admin
from events.models import Event,Project,TeamMember,Partner,PastEvent,Slider
from django.contrib import messages
admin.site.register(Event)
admin.site.register(Project)
admin.site.register(TeamMember)
admin.site.register(Partner)
# Register your models here.

def retrieveProjects(modeladmin, request, queryset):
  for obj in queryset:
    obj.retrieveProjects()


class PastEventAdmin(admin.ModelAdmin):
    actions = [retrieveProjects]
    def save_model(self, request, obj, form, change):
      obj.save()
      
      if 'source_projects' in form.changed_data:
        obj.retrieve_projects()
      retrieveProjects.short_description = "Parse devpost to get cache all the associated projects"
     
class SliderAdmin(admin.ModelAdmin):
    class Media:
      js = (
          'bower_components/tinymce/tinymce.min.js',
          'javascript/tinymceinit.js'  # app static folder
      )

    list_display = ('name','slider_location', 'order', 'main_text')
    
    fieldsets = [
        ('Required',               {'fields': ['name', 'photo', 'main_text','order', 'slider_location']}),
        ('Link 1 (Optional)',               {'fields': ['first_link_text', 'first_link']}),
        ('Link 2 (Optional)', {'fields': ['second_link_text', 'second_link']}),
        ('Variation', {'fields': ['overlay_percentage', 'add_call_to_action','align_left']}),
    ]

admin.site.register(PastEvent, PastEventAdmin)
admin.site.register(Slider, SliderAdmin)