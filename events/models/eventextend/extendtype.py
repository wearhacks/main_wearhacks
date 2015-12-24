from django.db import models

# Define types for the extensions
# (this is generic so can be used for any model that needs extensions)
class ExtendType(models.Model):
	type = models.CharField(max_length='50',
		help_text = 'Give a name to your custom type.')

	def __unicode__(self):
		return u"%s" % self.type

	class Meta:
		app_label = 'events'