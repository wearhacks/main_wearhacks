from django.db import models
from django.core.validators import MinValueValidator

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
	icon = models.CharField(max_length='50', blank=True, null=True,
		help_text = 'Icon for displaying on the front end (use fa icons).')
	priority = models.IntegerField(validators=[MinValueValidator(0)],
		help_text="The order for the extension to appear on the page.")
	format = models.CharField(max_length='50', blank=True, null=True,
		help_text = 'Text to add around the value. Use [v] to indicate where the value should be added.')

	def __unicode__(self):
		return u"%s: %s" % (self.key, self.description)

	class Meta:
		app_label = 'events'

	def save(self, *args, **kwargs):
	 	validate_extension_type(self)
	 	if len(self.icon) < 1:
	 		self.icon = None
		super(EventExtendType, self).save(*args, **kwargs)
