from django.db import models

class Ticket(models.Model):
	title = models.CharField(max_length = 100)
	price = models.FloatField()
	event = models.ForeignKey('Event', on_delete=models.CASCADE)

	def __unicode__(self):
		return u"%s - $%d" % (self.title, self.price)

	class Meta:
		app_label = 'events'