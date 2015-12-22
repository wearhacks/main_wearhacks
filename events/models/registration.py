# from django.db import models
# from django.utils.translation import ugettext_lazy as _
# from django.utils.translation import pgettext_lazy as __
# from django.conf import settings

# from django.core.validators import RegexValidator#, URLValidator
# from django.core.exceptions import ValidationError

# from django.core.urlresolvers import reverse
# from django.db.models import permalink

# import re

# def validate_true(value):
#     if not value:
#         raise ValidationError(_('This field must be checked'))

# class Registration(models.Model):
#     alpha = RegexValidator(regex=re.compile(r'^[\w\s]*$', flags=re.UNICODE), message=_('Only letters are allowed.'))

#     first_name = models.CharField(max_length=20, validators=[alpha],
#         verbose_name=_('first name'))
#     last_name = models.CharField(max_length=20, validators=[alpha],
#         verbose_name=_('last name'))
#     email = models.EmailField(verbose_name=_('email'))
#     # use an extension model to add more custom fields

#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     has_read_conditions = models.BooleanField(default=False,
#         validators = [validate_true])

#     is_email_sent = models.BooleanField(
#         default=False,
#         verbose_name= 'Was the confirmation email sent?',
#     )

#     # Ticket Info
#     ticket = models.ForeignKey('Ticket')
#     charge_attempt = models.ForeignKey('ChargeAttempt', blank=True, null=True)
#     # Add event? it's reachable from ticket, but if we allow many-to-one
#     # relationship between ticket and event, then it's better to have event fk here

#     # Logistics
#     ORDER_ID_MAX_LENGTH = 6
#     order_id = models.CharField(default='xxx', max_length=ORDER_ID_MAX_LENGTH)

#     has_attended = models.BooleanField(default=False)
#     staff_comments = models.TextField(max_length=100, default="No comments",
#         help_text='Log anything to do with this registration here.',
#         blank=True)

#     def fullName(self):
#         return '%s %s' % (self.first_name.encode('utf-8'),
#             self.last_name.encode('utf-8'))

#     # full_name.admin_order_field = 'last_name'

#     def needsToBeChecked(self):
#         result = False
#         if self.is_email_sent and self.charge and \
#             not self.charge.is_captured:
#             result = True
#         return result

#     def isCharge(self):
#         return bool(self.charge) and self.charge.is_captured

#     @staticmethod
#     def generate_order_id():
#         from random import randint
#         n, generated, order_id = Registration.ORDER_ID_MAX_LENGTH, False, 'xxx'
#         while not generated:
#             order_id = ''.join(["%s" % randint(0, 9) for num in range(0, n)])
#             if not Registration.objects.filter(order_id=order_id).exists():
#                 generated = True
#         return order_id

#     def get_confirmation_url(self):
#         """
#         Staff-only url to confirm registration
#         """
#         url = reverse("confirm-registration", kwargs={'order_id': str(self.order_id)})
#         full_url = ''.join([settings.HTTP_PREFIX, settings.HOSTS[0], url])
#         return full_url

#     def get_qrcode_url(self):
#         """
#         Access hacker mobile ticket
#         """
#         url = reverse("qrcode", kwargs={'order_id': str(self.order_id)})
#         full_url = ''.join([settings.HTTP_PREFIX, settings.HOSTS[0], url])
#         return full_url

#     def get_absolute_url(self):
#         return reverse("confirmation_email", kwargs={'order_id': str(self.order_id)})


#     class Meta:
#         ordering = ('-updated_at', 'last_name', 'first_name',)
#         app_label = 'events'

#     def __unicode__(self):
#         if self.pk:
#             return '{0} (#{1})'.format(self.full_name(), self.pk) #'{0}'.format(self.pk)
#         else:
#             return '{0} (Not saved)'.format(self.full_name())

