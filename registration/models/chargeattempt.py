from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import pgettext_lazy as __
from django.conf import settings

from django.core.validators import RegexValidator#, URLValidator
from django.core.exceptions import ValidationError


class ChargeAttempt(models.Model):
    # Required fields
    email = models.EmailField()
    charge_id = models.CharField(max_length=27)
    amount = models.IntegerField()

    created_at = models.DateTimeField(auto_now_add=True)

    # optional fields
    hacker = models.CharField(max_length=200, default='Unknown')
    is_livemode = models.BooleanField(default=False)
    is_paid = models.BooleanField(default=False)
    is_captured = models.BooleanField(default=False)

    status = models.CharField(max_length=100, default='No Status')
    source_id = models.CharField(max_length=29)

    # error logging (optional)
    failure_message = models.CharField(default='No Error', max_length=200,
        help_text='Charge object failure message', blank=True)
    failure_code = models.CharField(default='200', max_length=200,
        help_text='Charge object failure code', blank=True)
    error_http_status = models.CharField(default='200', max_length=4, blank=True)
    error_type = models.CharField(default='None', max_length=200,
        help_text='The type of error returned. Can be invalid_request_error, api_error, or card_error', blank=True)
    error_code = models.CharField(default='None', max_length=200,
        help_text='For card errors, a short string from amongst those listed on the right describing the kind of card error that occurred.', blank=True)
    error_param = models.CharField(default='None', max_length=200,
        help_text='The parameter the error relates to if the error is parameter-specific.', blank=True)
    error_message = models.CharField(default='None', max_length=300,
        help_text='A human-readable message giving more details about the error.', blank=True)
    SERVER_MESSAGE_MAX_LENGTH = 300
    server_message = models.TextField(default='', max_length=SERVER_MESSAGE_MAX_LENGTH,
        help_text='Message detailing internal server errors for debugging purposes', blank=True)


    def appendSaveServerMessage(self, message, exception=None):
        if self.server_message:
            message = self.server_message + '; ' + message
        if len(server_message) > ChargeAttempt.SERVER_MESSAGE_MAX_LENGTH:
            self.server_message = "...%s" % (server_message[-(n-3):])
        else:
            self.server_message = server_message

        if exception and hasattr(exception, 'json_body') and 'error' in exception.json_body:
            err = exception.json_body['error']
            err_fields = ('type', 'code', 'param', 'message')
            for f in err_fields:
                if f in err:
                    self.fields['error_' + f] = err[f]

            if hasattr(exception, 'http_status'):
                self.error_http_status = exception.http_status

        self.save()

    @property
    def registration(self):
        qs = Registration.objects.filter(charge=self)
        if qs.exists():
            return qs.first()
        else:
            return None

    class Meta:
        ordering = ('-created_at',)
        app_label = 'registration'

    def __unicode__(self):
        if self.registration and self.pk:
            return 'Attempt #%i by %s %s' % (self.pk, self.registration.first_name,
                self.registration.last_name)
        else:
            if self.pk:
                return 'Attempt #%i by %s' % (self.pk, self.hacker)
            else:
                return 'Attempt by %s' % (self.hacker)