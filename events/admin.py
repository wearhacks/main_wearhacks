from django.contrib import admin
from django import forms
from events.models import Event,Project,TeamMember,Partner,PastEvent,\
    Ticket,Registration,ChargeAttempt,EventPicture,EventContent
admin.site.register(Project)
admin.site.register(TeamMember)
admin.site.register(Partner)
admin.site.register(Registration)
admin.site.register(Ticket)
admin.site.register(ChargeAttempt)
admin.site.register(EventPicture)
admin.site.register(EventContent)

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

class TicketsInLine(admin.TabularInline):
    model = Ticket
    extra = 0

class EventContentsInLine(admin.TabularInline):
    model = EventContent
    extra = 0
    ordering = ("priority",)

class EventPicturesInLine(admin.TabularInline):
    model = EventPicture
    extra = 0

class EventAdmin(admin.ModelAdmin):
    inlines = [
        EventPicturesInLine, EventContentsInLine, TicketsInLine
    ]

    def _tickets(self, obj):
        return obj.tickets.all().count()

admin.site.register(Event, EventAdmin)
