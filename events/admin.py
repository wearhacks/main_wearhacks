from django.contrib import admin
from events.models import Event,Project,TeamMember,Partner,Content

admin.site.register(Event)
admin.site.register(Project)
admin.site.register(TeamMember)
admin.site.register(Partner)
admin.site.register(Content)
# Register your models here.
