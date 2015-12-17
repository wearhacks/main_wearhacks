from django import forms

class PartnerForm(forms.Form):
    organization_name = forms.CharField(widget=forms.TextInput(attrs={'required':True}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'required':True}))
    message = forms.CharField(widget=forms.Textarea(attrs={'required':True}))
