from django.db import models
from django.core.validators import MinValueValidator
from tinymce import models as tinymce_models

# Long text extension (can use this for blog too)
class EventContent(models.Model):
	event = models.ForeignKey('Event', on_delete=models.CASCADE)
	priority = models.IntegerField(validators=[MinValueValidator(0)],
		help_text="The order for the content to appear on the page.")

	# small, medium, large column for foundation grid format
	SIZETYPES = (
        ('large-12', 'Full Width'),
        ('large-6 medium-12', 'Large Half Width'),
        ('medium-6 small-12', 'Large and Medium Half Width'),
        ('large-4 medium-6 small-12', 'Third Width'),
        ('large-3 medium-4 small-6', 'Forth Width'),
    )
	size = models.CharField(max_length='50', default='large-12', choices=SIZETYPES,
		help_text="Fondation column class for responsiveness.")

	html = tinymce_models.HTMLField()
	draft = models.BooleanField(default=False)

	def __unicode__(self):
		return u"%s" % self.html

	class Meta:
		app_label = 'events'