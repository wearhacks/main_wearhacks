from django.db import models
from django.core.validators import MinValueValidator

class Ticket(models.Model):
	title = models.CharField(max_length = 100)
	price = models.FloatField()
	event = models.ForeignKey('Event', on_delete=models.CASCADE)
	stock = models.IntegerField(validators=[MinValueValidator(-1)],
		help_text="Number of tickets available. -1 for infinite.")
	priority = models.IntegerField(validators=[MinValueValidator(0)],
		help_text="The order for the content to appear on the page.")

	def __unicode__(self):
		return u"%s - $%d" % (self.title, self.price)

	def displayedPrice(self):
		return '{:20,.2f}'.format(self.price)

	class Meta:
		app_label = 'events'