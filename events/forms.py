from django import forms
from django.utils.safestring import mark_safe

class PartnerForm(forms.Form):
    organization_name = forms.CharField(widget=forms.TextInput(attrs={'required':True}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'required':True}))
    message = forms.CharField(widget=forms.Textarea(attrs={'required':True}))

class RegisterForm(forms.Form):
    fist_name = forms.CharField(widget=forms.TextInput(attrs={'required':True}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'required':True}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'required':True}))

    def setTickets(self,ticketSet):
        self.fields['tickets'] = forms.ModelChoiceField(queryset=ticketSet,
            empty_label='-- select --', required=True)
        self.fields['has_read_conditions'] = forms.BooleanField(required=True,
            label = mark_safe('I have read and I agree with \
                the <a class="terms" href="#"> Terms and Conditions</a> and the \
                the <a class="conduct" href="#"> Code of Conduct</a> '))

