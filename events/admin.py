from django.contrib import admin
from events.models import Event,Project,TeamMember,Partner

admin.site.register(Event)
admin.site.register(Project)
admin.site.register(TeamMember)
admin.site.register(Partner)
# Register your models here.
