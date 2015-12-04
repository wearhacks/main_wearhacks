from django.contrib import admin
from events.models import Event,Project,TeamMember,Partner,PastEvent
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
     


admin.site.register(PastEvent, PastEventAdmin)