from django.contrib import admin
from django import forms
from events.models import Event,Project,TeamMember,Partner,PastEvent,\
    Ticket,EventPicture,EventContent,Slider
# from registration.models import Registration,ChargeAttempt
from django.contrib import messages
# from django.utils.safestring import mark_safe
# from tinymce.widgets import TinyMCE


admin.site.register(Project)
admin.site.register(TeamMember)
admin.site.register(Partner)
# admin.site.register(Registration)
admin.site.register(Ticket)
# admin.site.register(ChargeAttempt)
#admin.site.register(EventPicture)
#admin.site.register(EventContent)

# Register your models here.

def retrieveProjects(modeladmin, request, queryset):
  for obj in queryset:
    obj.retrieveProjects()

# class EventContentInLineForm(forms.BaseInlineFormSet):
#     content = forms.CharField(widget=TinyMCE(attrs={'cols': 200, 'rows': 30}))

class TicketsInLine(admin.TabularInline):
    model = Ticket
    extra = 0

class EventContentsInLine(admin.TabularInline):
    model = EventContent
    extra = 0
    ordering = ("priority",)
    # formset = EventContentInLineForm

class EventPicturesInLine(admin.TabularInline):
    model = EventPicture
    extra = 0
    fields = ('photo','render_image')
    readonly_fields = ('render_image',)

    def render_image(self, obj):
        return '%s' % obj.photo.url

class EventAdmin(admin.ModelAdmin):
    list_display = ('event_name', 'start_date', 'end_date')
    inlines = [EventPicturesInLine, EventContentsInLine, TicketsInLine]
    def _tickets(self, obj):
        return obj.tickets.all().count()

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

    list_display = ('slider_location', 'name', 'order', 'main_text')

    fieldsets = [
        ('Required',               {'fields': ['name', 'photo', 'main_text','order', 'slider_location']}),
        ('Link 1 (Optional)',               {'fields': ['first_link_text', 'first_link']}),
        ('Link 2 (Optional)', {'fields': ['second_link_text', 'second_link']}),
        ('Variation', {'fields': ['overlay_percentage', 'add_call_to_action','align_left']}),
    ]

admin.site.register(PastEvent, PastEventAdmin)
admin.site.register(Slider, SliderAdmin)
admin.site.register(Event, EventAdmin)

