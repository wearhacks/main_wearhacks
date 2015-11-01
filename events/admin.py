from django.contrib import admin
from events.models import Event,Project,TeamMember

admin.site.register(Event)
admin.site.register(Project)
admin.site.register(TeamMember)
# Register your models here.
