from django.contrib import admin
from events.models import Event,Project,TeamMember,Partner,EventPicture

admin.site.register(Event)
admin.site.register(Project)
admin.site.register(TeamMember)
admin.site.register(Partner)
admin.site.register(EventPicture)
# Register your models here.
