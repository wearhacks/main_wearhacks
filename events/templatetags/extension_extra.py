from django import template

register = template.Library()

@register.filter(name='get_extension')
def get_extension(event, extendKey):
	print extendKey
	return event.getExtension(extendKey)