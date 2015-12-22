from django.db import models

from extensionhelpers import validate_extension_type

# Define allowed type for event extensions
# This is like an extended version of the ExtendType
class EventExtendType(models.Model):
	key = models.CharField(max_length='50',
		help_text = 'Keyword to name this extension.')
	type = models.ForeignKey('ExtendType', on_delete=models.CASCADE)
	description = models.CharField(max_length='250',
		help_text = 'Short description of what this extensions is about.')
	values = models.CharField(max_length='250', blank=True, null=True,
		help_text = 'Allowed values (for list, delimetered by comma.')

	def __unicode__(self):
		return u"%s" % self.key

	class Meta:
		app_label = 'events'

	def save(self, *args, **kwargs):
	 	validate_extension_type(self)
		super(EventExtendType, self).save(*args, **kwargs)
