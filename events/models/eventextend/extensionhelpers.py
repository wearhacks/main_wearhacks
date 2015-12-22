from django.core.exceptions import ValidationError

# Generic validators for extensions according to their type

# for saving extension
def validate_extension(extension):
	value = extension.value
	extendType = extension.extendKey
	typeKey = extendType.type.type
	if typeKey == 'number' and not value.replace('.','',1).isdigit():
		raise ValidationError('%s is not a valid number' % value)
	if typeKey == 'list':
		allowedVal = extendType.values.split(',')
		if not value in allowedVal:
			raise ValidationError('%s is not an allowed value for type %s' % (extendType.key, value))

# for saving extension type
def validate_extension_type(extensionType):
	typeKey = extensionType.type.type
	if typeKey == 'list' and len(extensionType.values) < 1:
		raise ValidationError('Need at least one value for list type.')