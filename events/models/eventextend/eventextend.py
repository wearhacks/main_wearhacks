from django.db import models

from extensionhelpers import validate_extension

# Data for the extensions
class EventExtend(models.Model):
	value = models.TextField(help_text = 'Extension value')
	extendKey = models.ForeignKey('EventExtendType', on_delete=models.CASCADE,
		help_text = 'Extension key')
	event = models.ForeignKey('Event', on_delete=models.CASCADE)

	def __unicode__(self):
		if self.extendKey.format:
			formatted = self.extendKey.format.replace('[v]', self.value)
			return u"%s" % formatted
		return u"%s" % self.value

	class Meta:
		app_label = 'events'

	def save(self, *args, **kwargs):
		validate_extension(self)
		super(EventExtend, self).save(*args, **kwargs)
