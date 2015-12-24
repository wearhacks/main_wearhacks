from django.core.exceptions import ValidationError


def _import(name):
    components = name.split('.')
    mod = __import__(components[0])
    model = getattr(mod, 'models')
    return getattr(model, components[1])

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
	if typeKey == 'modelpk':
		modelClass = _import(extendType.values)
		try:
			modelClass.objects.get(pk=int(value))
		except:
			raise ValidationError('Cannot find row %s in model %s' % (value, extendType.values))


# for saving extension type
def validate_extension_type(extensionType):
	typeKey = extensionType.type.type
	if len(extensionType.values) < 1:
		if typeKey == 'list':
			raise ValidationError('Need at least one value for list type.')
		if typeKey == 'modelpk':
			raise ValidationError('Need a model class name as the value for the modelpk type.')