from django.views import generic
from django.views.decorators.csrf import csrf_exempt

from django.core.mail import EmailMultiAlternatives
from django.core.urlresolvers import reverse
from django.core.files import File
from django.core.files.storage import default_storage

from django.shortcuts import render, get_object_or_404

from django.template import Context
from django.template.loader import render_to_string
from django.conf import settings

from django.utils import translation
from django.utils.translation import ugettext as _
from django.utils.translation import pgettext as __

from django.http import HttpResponse,JsonResponse

from ..models import Registration, ChargeAttempt#, Challenge
from events.models import Event, Ticket
from ..forms import WorkshopRegistrationForm

from ..views.email import QRCodeView, TicketView, ConfirmationEmailView


# from crispy_forms.utils import render_crispy_form
# from jsonview.decorators import json_view

from tempfile import TemporaryFile
import os
import stripe
from time import gmtime, strftime

# def get_stripe_secret_key(self):
#     return settings.STRIPE_SECRET_KEY

# def get_stripe_public_key(self):
#     return settings.STRIPE_PUBLIC_KEY

def getEventTicket(ticket_pk, event):
    return event.ticket_set.filter(pk=ticket_pk).first()
    # if ticket.len() == 0:
    #     return False
    # return ticket

def badForm():
    return JsonResponse('Please correct your registration information before proceeding.', status=400)

def badTicketResponse():
    return JsonResponse('Invalid ticket.', status=400)

def generateErrorResponse(message):
    return JsonResponse(message, status=400)

def successCheckoutResponse():
    return JsonResponse('A confirmation email will be sent shortly.', status=200)

def successTicketCheckResponse(ticket):
    print settings.TEST_STRIPE_PUBLIC_KEY
    return JsonResponse({
            'price': ticket.price,
            'name': ticket.title,
            'key': settings.STRIPE_PUBLIC_KEY
        }, status=200)

def saveAndLogError(self, charge_attempt, message, e):
    if charge_attempt:
        charge_attempt.appendSaveServerMessage(message, exception=e)
    print e

def callStripe(registration, charge_attempt, token_id, order_id):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    hacker = "%s %s" % (registration['first_name'], registration['last_name'])

    try:
        charge = stripe.Charge.create(
            amount=charge_attempt.amount,
            currency="cad",
            source=token_id, # obtained with Stripe.js
            description="Charge for %s" % hacker,
            receipt_email=registration['email'],
            statement_descriptor=registration['ticket'].event.event_name,
            capture=False,
            metadata = {
                'Name': hacker,
                'Charge Attempt ID': charge_attempt.pk,
                'Order ID': order_id
            }
        )

        # update charge attempt fields with Stripe charge fields
        if charge:
            update_fields = {
                'charge_id': charge.id,
                'is_livemode': charge.livemode,
                'is_paid': charge.paid,
                'status': charge.status,
                'amount': charge.amount,
                'source_id': charge.source.id,
                'is_captured': charge.captured,
                'failure_message': charge.failure_message or '',
                'failure_code': charge.failure_code or ''
            }
        charge_attempt.update(update_fields)
        return (True, charge_attempt)

    except stripe.error.CardError, e:
        # Since it's a decline, stripe.error.CardError will be caught
        saveAndLogError(charge_attempt,'Stripe Card Error', e)
        return (False, "Something went wrong on Stripe's end.")

    except (stripe.error.InvalidRequestError, stripe.error.AuthenticationError), e:
        # invalid_request: Invalid parameters were supplied to Stripe's API OR
        # authetication_error: Authentication with Stripe's API failed
        # (maybe you changed API keys recently) OR
        saveAndLogError(charge_attempt,'Stripe Request Error', e)
        return (False, 'Something went wrong on our end.')

    except stripe.error.APIConnectionError, e:
        # Authentication with Stripe's API failed
        # (maybe you changed API keys recently)
        saveAndLogError(charge_attempt,'API Connection Error', e)
        return (False, 'Network communication with Stripe failed.')

    except stripe.error.StripeError, e:
        saveAndLogError(charge_attempt,'Stripe Error', e)
        return (False, "Something went wrong on Stripe's end.")

    except Exception, e:
        saveAndLogError(charge_attempt,'Error while creating Stripe charge', e)

    return (False, 'WTF dunno wat happened')

def chargeUser(charge, charge_attempt):
    try:
        charge = stripe.Charge.retrieve(charge.id)
        charge.capture()
        charge_attempt.is_captured = True
        charge_attempt.save()
        return (True,)
    except Exception, e:
        saveAndLogError(charge_attempt, 'Failed while capturing charge.', e)
        return (False, 'We could not charge you.')


def send_confirmation_email(registration):
    import os

    # create context
    d = ConfirmationEmailView.get_extra_context(registration)
    c = Context(d)

    # create html/txt
    msg_plaintext = render_to_string('registration/confirmation_email.txt', c)
    msg_html      = render_to_string('registration/confirmation_email.html', c)

    # email settings
    subject = _('Thanks for signing up!')
    from_email = "WearHacks Montreal <%s>" % settings.DEFAULT_FROM_EMAIL
    to = [registration.email]
    headers = {'Reply-To': _("WearHacks Montreal Team <montreal@wearhacks.com>")} #TODO: change this
    # maybe add a contact email field for each event if different email per event?

    # mandrill settings
    tags = ['registration confirmation']
    # if settings.DEBUG:
    #   tags.append('test')
    # if registration.is_early_bird:
    #   tags.append('early bird')
    # else:
    #   tags.append('student')
    metadata = {'order_id': registration.order_id}

    # ticket
    ticket_file_path = os.path.join(settings.SITE_ROOT, registration.ticket_file.path)

    # try:
    #     fn = ''
    #     directory = os.path.join(settings.SITE_ROOT, 'media', 'orders')
    #     if not os.path.exists(directory):
    #         os.makedirs(directory)
    #     fn = os.path.join(directory, registration.order_id + '.html')
    #     with open(fn, 'w') as f:
    #         f.write(msg_html)
    # except Exception, e:
    #     if fn:
    #         print "Could not write to %s" % (fn)
    #     print 'ERROR: %s' % (str(e))

    msg = EmailMultiAlternatives(
        subject=subject,
        body=msg_plaintext,
        from_email=from_email,
        to=to,
        reply_to=[from_email],
        headers=headers # optional extra headers
    )
    msg.attach_alternative(msg_html, "text/html")
    msg.attach_file(ticket_file_path)
    msg.tags = tags
    msg.metadata = metadata

    if not settings.DEBUG and not (hasattr(settings,'FAKE_SEND_EMAIL') and settings.FAKE_SEND_EMAIL):
        msg.send()
    else:
        print 'Registration email at: %s ' % (
            reverse('confirmation_email', kwargs={'order_id' : registration.order_id}))

def generate_pdf_ticket():
    import cStringIO as StringIO
    import ho.pisa as pisa
    from django.template.loader import get_template
    from django.template import Context
    from django.http import HttpResponse
    from cgi import escape

    def render_to_pdf(template_src, context_dict):
        template = get_template(template_src)
        context = Context(context_dict)
        html  = template.render(context)
        result = StringIO.StringIO()

        pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("ISO-8859-1")), result)
        if not pdf.err:
            return HttpResponse(result.getvalue(), content_type='application/pdf')
        return HttpResponse(_('We had some errors<pre>%s</pre>') % escape(html))

def sendConfirmationEmail(new_registration, charge_attempt):
    try:
        QRCodeView.generate_qr_code(registration=new_registration)
        TicketView.generate_pdf_ticket(registration=new_registration)
        print "Sending confirmation email..."
        send_confirmation_email(new_registration)
        return (True,)
    except Exception, e:
        saveAndLogError(charge_attempt,
            'Failed while sending confirmation email (order #%s).' % (new_registration.order_id), e)
        return (False, 'Your confirmation email cannot be sent at the moment. '
            '</strong><small>Everything else went smoothly and your '
            'payment went through. Admins have been notified and '
            'will send you a confirmation email shortly.</small>')


# these should usually be called form ajax
@csrf_exempt
def ticket(request):
    if request.method == 'POST':
        event_slug = request.POST.get('event_slug')
        ticket_id = request.POST.get('ticket_id')
        if not event_slug or not ticket_id:
            return redirect('events')
        event = Event.objects.get(slug = event_slug)
        ticket = getEventTicket(ticket_id, event)
        if not ticket:
            return badTicketResponse()
        else:
            return successTicketCheckResponse(ticket)


@csrf_exempt
def register(request, event_slug=None):
    if event_slug and request.method == 'POST':
        try:
            event = Event.objects.get(slug = event_slug)
            form = WorkshopRegistrationForm(None, request.POST)
            if form.is_valid():
                ticket = getEventTicket(form.cleaned_data['tickets'].id, event)
                if not ticket:
                    return badTicketResponse()

                token_id = request.POST.get('token_id', None)
                print token_id
                # order_id = request.POST.get('order_id', 'xxx')
                order_id = Registration.generate_order_id()
                if not token_id:
                    pass
                    # TODO
                registration_field = {
                    'first_name': form.cleaned_data['first_name'],
                    'last_name': form.cleaned_data['last_name'],
                    'email': form.cleaned_data['email'],
                    'ticket': ticket,
                    'order_id':order_id
                }

                charge_attempt_fields = {
                    'amount': ticket.price,
                    'source_id': token_id
                }

                charge_attempt = ChargeAttempt.objects.create(**charge_attempt_fields)
                charge_attempt.save()

                success, obj = callStripe(registration_field, charge_attempt, token_id, order_id)
                if not success:
                    return generateErrorResponse(_(obj
                        +"</br>Please refresh and try again. <strong>Don't worry, you haven't been charged.</strong>"))

                success, message = chargeUser(charge, charge_attempt)
                if not success:
                    return generateErrorResponse(message)

                registration_field['charge_attempt'] = obj
                registration = Registration.objects.create(**registration_field)
                registration.save()

                success, message = sendConfirmationEmail(registration, charge_attempt)
                if not success:
                    return generateErrorResponse(message)

                return successCheckoutResponse()
            else:
                return badForm()

        except ObjectDoesNotExist:
            return redirect('events')

    return redirect('events')

# from django.views import generic

# from django.core.mail import EmailMultiAlternatives
# from django.core.urlresolvers import reverse
# from django.core.files import File
# from django.core.files.storage import default_storage

# from django.shortcuts import render, get_object_or_404

# from django.template import Context
# from django.template.loader import render_to_string
# from django.conf import settings

# from django.utils import translation
# from django.utils.translation import ugettext as _
# from django.utils.translation import pgettext as __

# from registration.models import Registration, ChargeAttempt, Challenge
# from registration.forms import RegistrationForm

# from registration.views.email import QRCodeView, TicketView, ConfirmationEmailView

# from crispy_forms.utils import render_crispy_form
# from jsonview.decorators import json_view

# from tempfile import TemporaryFile
# import os
# import stripe
# from time import gmtime, strftime

# class RegistraionClosed(generic.TemplateView):
#     template_name = 'registration/closed.html'

# class SubmitRegistrationView(generic.View):
#     template_name = 'registration/form.html'
#     form_class = RegistrationForm

#     def get_stripe_secret_key(self):
#         return settings.STRIPE_SECRET_KEY

#     def get_stripe_public_key(self):
#         return settings.STRIPE_PUBLIC_KEY

#     def get(self, request, *args, **kwargs):
#         language = request.LANGUAGE_CODE
#         challenge = Challenge.get_unsolved_challenge(language=language)
#         challenge_id = challenge.id if challenge else None
#         order_id = Registration.generate_order_id()
#         context = {
#             'order_id': order_id,
#             'form': RegistrationForm(challenge=challenge),
#             'stripe_public_key': self.get_stripe_public_key(),
#             'challenge_id': challenge_id
#         }
#         print 'GET ====== '
#         return render(request, self.template_name, context)

#     def get_language(self, request):
#         language = request.POST.get('lang', settings.LANGUAGE_CODE)
#         translation.activate(language)
#         request.LANGUAGE_CODE = language
#         return (request, language)

#     @json_view
#     def post(self, request, *args, **kwargs):
#         print '*' * 100
#         print strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())
#         request, language = self.get_language(request)
#         order_id = request.POST.get('order_id', 'xxx')

#         charge_attempt = None
#         checkout_success = False
#         success_message = ''
#         checkout_message = _('Checkout not attempted yet.')
#         fraud_attempt = False
#         error_message = ''
#         email = None
#         server_error = False
#         server_message_client = ''
#         server_messages = []
#         is_captured = False

#         has_solved_challenge = False

#         if settings.DEBUG:
#             # auto fill some fields
#             defaults = (
#                     ('first_name', 'First'),
#                     ('last_name', 'Last'),
#                     ('email', settings.EMAIL_HOST_USER),
#                     ('gender', 'N'),
#                     ('tshirt_size', 'M'),
#                 )
#             for k, v in defaults:
#                 if not request.POST[k]:
#                     request.POST[k] = v
#             request.POST['has_read_conditions'] = True

#         # check registration information
#         registration_success= False
#         registration_message = ''

#         challenge_id = request.POST.get('challenge_id', None)
#         if Challenge.objects.filter(id=challenge_id).exists():
#             challenge = Challenge.objects.get(id=challenge_id)
#         else:
#             challenge = None

#         discount_code = None
#         ticket_price = Registration.TICKET_FULL_PRICE
#         form = self.form_class(request.POST, request.FILES, challenge=challenge)

#         if form.is_valid():
#             registration_success = True
#             email = form.cleaned_data['email']
#             has_solved_challenge = form.cleaned_data['has_solved_challenge']
#             discount_code = form.discount_code
#         else:
#             registration_message= _('Please correct your registration information'
#                 ' before proceeding.')

#         # save resume to temporary file if submitted
#         if 'resume' in request.FILES and 'resume' in form.cleaned_data:
#             self.save_resume(form.cleaned_data['resume'], order_id)

#         form_html = render_crispy_form(form)

#         # get pricing info
#         discount = {'percentage': 0, 'amount': 0}
#         if registration_success:
#             is_student = form.cleaned_data['is_student']
#             ___, ___, ticket_price, discount = self.get_ticket_info(is_student, discount_code=discount_code)

#         if has_solved_challenge or ticket_price == 0:
#             success_message += _('Congrats, you have a free ticket! ')
#             checkout_success = True

#         # check amount is valid
#         amount = int(request.POST.get('amount', 0))
#         is_valid_amount = False
#         if not has_solved_challenge:
#             if amount:
#                 is_student = request.POST.get('is_student', False)
#                 ___, ___, ticket_price, __ = self.get_ticket_info(is_student, discount_code=discount_code)
#                 is_valid_amount = amount == ticket_price
#             if amount and not is_valid_amount:
#                 checkout_success = False
#                 checkout_message = '<strong>%s </strong> </br>' % (
#                     _('</br>r u trying to hack us? u wot m8'))

#                 fraud_attempt = True
#                 server_messages.append("Fraud attempt: amount entered was %.2f$" % (amount * 0.01))

#         # attempt charge only if registration information is valid
#         if registration_success and is_valid_amount and not has_solved_challenge and ticket_price > 0:
#             token_id = request.POST.get('token_id', None)
#             charge = None
#             charge_attempt = None
#             e = None # Exception variable

#             if not token_id:
#                 # no token id is sent during form prevalidation
#                 # this is normal
#                 registration_message = _('Registration Information Valid')
#                 checkout_message = ''
#             else:
#                 try:
#                     hacker_name = "%s %s" % (
#                         form.cleaned_data["first_name"],
#                         form.cleaned_data["last_name"])

#                     charge_attempt_fields = {
#                         'hacker': hacker_name,
#                         'charge_id': 'xxx',
#                         'email': email,
#                         'amount': amount,
#                         'source_id': token_id
#                     }

#                     charge_attempt = ChargeAttempt.objects.create(**charge_attempt_fields)
#                     charge_attempt.save()

#                     charge_attempt_link = 'http://%s/admin/registration/chargeattempt/%i/' % (
#                             'montreal.wearhacks.com',
#                             charge_attempt.pk
#                         )
#                     if not fraud_attempt:
#                         stripe.api_key = self.get_stripe_secret_key()
#                         charge = stripe.Charge.create(
#                           amount=amount,
#                           currency="cad",
#                           source=token_id, # obtained with Stripe.js
#                           description="Charge for %s" % (hacker_name),
#                           receipt_email=email,
#                           statement_descriptor="WearHacks Mtl 2015",
#                           capture=False,
#                           metadata = {
#                               'Name': hacker_name,
#                               'Charge Attempt ID': charge_attempt.pk,
#                               'Charge Attempt Link': charge_attempt_link,
#                               'Order ID': order_id
#                           }
#                         )

#                         # update charge attempt fields with Stripe charge fields
#                         if charge:
#                             update_fields = {
#                                 'charge_id': charge.id,
#                                 'is_livemode': charge.livemode,
#                                 'is_paid': charge.paid,
#                                 'status': charge.status,
#                                 'amount': charge.amount,
#                                 'source_id': charge.source.id,
#                                 'is_captured': charge.captured,
#                                 'failure_message': charge.failure_message or '',
#                                 'failure_code': charge.failure_code or ''
#                             }
#                             charge_attempt_fields.update(update_fields)

#                         checkout_success = True
#                 except stripe.error.CardError, e:
#                     # Since it's a decline, stripe.error.CardError will be caught
#                     body = e.json_body
#                     err  = body['error']
#                     error_http_status = e.http_status
#                     checkout_message = _("Something went wrong on Stripe's end. </br>")
#                     checkout_success = False
#                     self._save_server_message_to_charge_attempt(charge_attempt,
#                         ['Stripe Card Error'], e)

#                 except (stripe.error.InvalidRequestError,
#                     stripe.error.AuthenticationError), e:
#                     # invalid_request: Invalid parameters were supplied to Stripe's API OR
#                     # authetication_error: Authentication with Stripe's API failed
#                     # (maybe you changed API keys recently) OR
#                     checkout_message = _('Something went wrong on our end. </br>')
#                     server_error = True
#                     checkout_success = False
#                     print e
#                     self._save_server_message_to_charge_attempt(charge_attempt,
#                         ['Stripe Request Error'], e)

#                 except stripe.error.APIConnectionError, e:
#                     # Authentication with Stripe's API failed
#                     # (maybe you changed API keys recently)
#                     checkout_message = _('Network communication with Stripe '
#                         'failed. </br>')
#                     checkout_success = False
#                     print e
#                     self._save_server_message_to_charge_attempt(charge_attempt,
#                         ['API Connection Error'], e)

#                 except stripe.error.StripeError, e:
#                     checkout_message = _("Something went wrong on Stripe's end. </br>")
#                     checkout_success = False
#                     print e
#                     self._save_server_message_to_charge_attempt(charge_attempt,
#                         ['Stripe Error'], e)

#                 except Exception, e:
#                     checkout_message = ''
#                     server_error = True
#                     checkout_success = False
#                     print e
#                     self._save_server_message_to_charge_attempt(charge_attempt,
#                         ['Error while creating Stripe charge'], e)

#                 # if charge creation returns errors, log them to charge attempt
#                 if e:
#                     if hasattr(e, 'json_body') and 'error' in e.json_body:
#                         err = e.json_body['error']
#                         err_fields = ('type', 'code', 'param', 'message')
#                         for f in err_fields:
#                             if f in err:
#                                 charge_attempt_fields['error_' + f] = err[f]
#                         checkout_message += '<strong>%s</strong> </br>' % (err["message"])

#                     if hasattr(e, 'http_status'):
#                         charge_attempt_fields['error_http_status'] = e.http_status

#                 # add more information to client-side messages
#                 if not checkout_success:
#                     if charge and hasattr(charge, 'failure_message') and charge.failure_message is not None:
#                         checkout_message += charge.failure_message
#                     checkout_message += _("Please refresh and try again.")
#                     if not checkout_success and not is_captured:
#                         checkout_message += _("</br><strong>Don't worry, you haven't been charged.</strong>")

#                 # save charge attempt
#                 if charge_attempt:
#                     for k, v in charge_attempt_fields.iteritems():
#                         setattr(charge_attempt, k, v)
#                     charge_attempt.save()

#         new_registration = None
#         if registration_success and checkout_success and not server_error:
#             try:
#                 # Save registration
#                 new_registration = form.save()

#                 # if the form does not have a resume, attempt to retrieve it
#                 if not bool(new_registration.resume):
#                     self.retrieve_resume(new_registration, order_id)

#                 if has_solved_challenge:
#                     challenge = form.cleaned_data['solved_challenge']
#                     challenge.solved = True
#                     challenge.save()
#                     new_registration.solved_challenge = form.challenge
#                     new_registration.has_solved_challenge = True
#                 if form.discount_code:
#                     new_registration.discount_code = form.discount_code

#                 # Add additional fields to form
#                 new_registration.preferred_language = language

#                 is_student = request.POST.get('is_student', False)
#                 is_early_bird, ticket_description, ticket_price, discount = self.get_ticket_info(
#                     is_student, has_solved_challenge=has_solved_challenge, discount_code=discount_code)

#                 new_registration.is_early_bird = is_early_bird
#                 new_registration.ticket_description = ticket_description
#                 new_registration.ticket_price = ticket_price

#                 new_registration.order_id = order_id

#                 new_registration.charge = charge_attempt
#                 new_registration.is_waitlisted = True
#                 new_registration.save()
#             except Exception, e:
#                 server_error = True
#                 checkout_success = False
#                 server_message_client = self._get_server_error_message(
#                     _('Your registration could not be saved.'))
#                 server_messages.append('Failed while saving registration form.')
#                 self._save_server_message_to_charge_attempt(charge_attempt, server_messages, e)

#             # Charge user
#             is_captured = False
#             if not server_error and not has_solved_challenge and ticket_price > 0:
#                 try:
#                     charge = stripe.Charge.retrieve(charge.id)
#                     charge.capture()
#                     is_captured = True
#                     charge_attempt.is_captured = is_captured
#                     charge_attempt.save()
#                 except Exception, e:
#                     server_error = True
#                     server_message_client = self._get_server_error_message(
#                         _('We could not charge you.'),
#                         dont_worry=False)
#                     server_messages.append('Failed while capturing charge.')
#                     self._save_server_message_to_charge_attempt(charge_attempt, server_messages, e)

#             # Send confirmation email
#             if not server_error:
#                 try:
#                     QRCodeView.generate_qr_code(registration=new_registration)
#                     TicketView.generate_pdf_ticket(registration=new_registration)
#                     print "Sending confirmation email..."
#                     self.send_confirmation_email(new_registration)
#                 except Exception, e:
#                     server_error = True
#                     checkout_success = False
#                     server_message_client = self._get_server_error_message(_(
#                         'Your confirmation email cannot be sent at the moment. '
#                         '</strong><small>Everything else went smoothly and your '
#                         'payment went through. Admins have been notified and '
#                         'will send you a confirmation email shortly.</small>'
#                         '<strong>'), dont_worry=False, default_header=False )
#                     server_messages.append('Failed while sending confirmation email (order #%s).' % (new_registration.order_id))
#                     self._save_server_message_to_charge_attempt(charge_attempt, server_messages, e)

#             if not server_error:
#                 success_message += _('A confirmation email will be sent shortly.')
#                 try:
#                     new_registration.is_email_sent = True
#                     new_registration.is_waitlisted = True
#                     new_registration.save()
#                 except Exception, e:
#                     server_messages.append('Failed while setting is_email_sent to True in registration.')
#                     self._save_server_message_to_charge_attempt(charge_attempt, server_messages, e)

#         elif charge_attempt and len(server_messages) > 0:
#             self._save_server_message_to_charge_attempt(charge_attempt, server_messages, None)
#         # success_message += _('Thanks for signing up you crypto whizz')

#         response = {
#             'server_message': server_message_client,
#             'server_error': server_error,
#             'registration_success': registration_success,
#             'checkout_success': checkout_success,
#             'registration_message': registration_message,
#             'checkout_message': checkout_message,
#             'success': registration_success and checkout_success,
#             'success_message': success_message,
#             'stripe_public_key': self.get_stripe_public_key(),
#             'charge_amount': ticket_price,
#             'discount_percentage': discount['percentage'],
#             'discount_amount': discount['amount']
#         }
#         print response
#         if server_messages:
#             print ' / '.join(server_messages)
#         response['form_html'] = form_html

#         return response

#     def _get_checkout_error_message(self, inner_message, dont_worry=True, default_header=True):
#         message = ''
#         if default_header:
#             message += _('Oops, something went wrong on our end.</br>Please '
#                 'refresh and try again. If the problem persists, please contact'
#                 ' our support team. </br>')
#         message += "<strong>%s</strong>"
#         if dont_worry:
#             message += _("</br><strong>Don't worry, you haven't been charged.</strong>")
#         message = message % (inner_message)
#         return message

#     def _get_server_error_message(self, inner_message, dont_worry=True, default_header=True):
#         message = ''
#         if default_header:
#             message += _('Oops, something went wrong on our end.</br>Please '
#                 'refresh and try again. If the problem persists, please contact'
#                 ' our support team. </br>')
#         message += "<strong>%s</strong>"
#         if dont_worry:
#             message += _("</br><strong>Don't worry, you haven't been charged.</strong>")
#         message = message % (inner_message)
#         return message

#     def _save_server_message_to_charge_attempt(self, charge_attempt, messages, e):
#         if charge_attempt:
#             charge_attempt.save_server_message(messages, exception=e)

#     def get_ticket_info(self, is_student, discount_code=None, has_solved_challenge=False):
#         # early_bird_deadline = datetime.strptime('Sep 1 2015', '%b %d %Y')
#         # is_early_bird = datetime.now() < early_bird_deadline
#         is_early_bird = False

#         ticket_description, ticket_price, discount = Registration.get_ticket_info(
#                 is_student=is_student,
#                 is_early_bird=is_early_bird,
#                 has_solved_challenge=has_solved_challenge,
#                 discount_code=discount_code
#             )
#         return (is_early_bird, ticket_description, ticket_price, discount)


#     def _get_resume_path(self, order_id):
#         path = os.path.join(default_storage.location,
#             'resumes/tmp/%s.pdf' % (order_id))
#         return path

#     def save_resume(self, file, order_id):
#         path = self._get_resume_path(order_id)
#         # overwrite if file already exists
#         if default_storage.exists(path):
#             default_storage.delete(path)
#         default_storage.save(path, file)

#     def retrieve_resume(self, registration, order_id):
#         path = self._get_resume_path(order_id)
#         if default_storage.exists(path):
#             file = File(default_storage.open(path))
#             registration.resume.save('default.pdf', file, save=False)
#             return True
#         return False

#     def send_confirmation_email(self, registration):
#         import os

#         # create context
#         d = ConfirmationEmailView.get_extra_context(registration)
#         c = Context(d)

#         # create html/txt
#         msg_plaintext = render_to_string('registration/confirmation_email.txt', c)
#         msg_html      = render_to_string('registration/confirmation_email.html', c)

#         # email settings
#         subject = _('Thanks for signing up!')
#         from_email = "WearHacks Montreal <%s>" % settings.DEFAULT_FROM_EMAIL
#         to = [registration.email]
#         headers = {'Reply-To': _("WearHacks Montreal Team <montreal@wearhacks.com>")}

#         # mandrill settings
#         tags = ['registration confirmation']
#         if settings.DEBUG:
#             tags.append('test')
#         if registration.is_early_bird:
#             tags.append('early bird')
#         else:
#             tags.append('student')
#         metadata = {'order_id': registration.order_id}

#         # ticket
#         ticket_file_path = os.path.join(settings.SITE_ROOT, registration.ticket_file.path)

#         # try:
#         #     fn = ''
#         #     directory = os.path.join(settings.SITE_ROOT, 'media', 'orders')
#         #     if not os.path.exists(directory):
#         #         os.makedirs(directory)
#         #     fn = os.path.join(directory, registration.order_id + '.html')
#         #     with open(fn, 'w') as f:
#         #         f.write(msg_html)
#         # except Exception, e:
#         #     if fn:
#         #         print "Could not write to %s" % (fn)
#         #     print 'ERROR: %s' % (str(e))

#         msg = EmailMultiAlternatives(
#             subject=subject,
#             body=msg_plaintext,
#             from_email=from_email,
#             to=to,
#             reply_to=[from_email],
#             headers=headers # optional extra headers
#         )
#         msg.attach_alternative(msg_html, "text/html")
#         msg.attach_file(ticket_file_path)
#         msg.tags = tags
#         msg.metadata = metadata

#         if not settings.DEBUG and not (
#             hasattr(settings, 'FAKE_SEND_EMAIL') and settings.FAKE_SEND_EMAIL):
#             msg.send()
#         else:
#             print 'Registration email at: %s ' % (
#                 reverse('confirmation_email', kwargs={'order_id' : registration.order_id}))

#     def generate_pdf_ticket(self):
#         import cStringIO as StringIO
#         import ho.pisa as pisa
#         from django.template.loader import get_template
#         from django.template import Context
#         from django.http import HttpResponse
#         from cgi import escape


#         def render_to_pdf(template_src, context_dict):
#             template = get_template(template_src)
#             context = Context(context_dict)
#             html  = template.render(context)
#             result = StringIO.StringIO()

#             pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("ISO-8859-1")), result)
#             if not pdf.err:
#                 return HttpResponse(result.getvalue(), content_type='application/pdf')
#             return HttpResponse(_('We had some errors<pre>%s</pre>') % escape(html))

