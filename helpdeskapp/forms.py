from django import forms

from helpdeskapp.models import Ticket


class AddTicketForm(forms.ModelForm):
    title = forms.CharField(max_length=100)
    description = forms.CharField(widget=forms.Textarea)
    priority = forms.ChoiceField(choices=Ticket.STATUS_CHOICES2)
    request_type = forms.ChoiceField(choices=Ticket.STATUS_CHOICES3)
    

    
    class Meta:
        model = Ticket
        fields = ('title', 'description', 'priority', 'request_type')

class EditTicketForm(forms.ModelForm):
    title = forms.CharField(max_length=100)
    description = forms.CharField(widget=forms.Textarea)
    priority = forms.ChoiceField(choices=Ticket.STATUS_CHOICES2)
    request_type = forms.ChoiceField(choices=Ticket.STATUS_CHOICES3)
    status = forms.ChoiceField(choices=Ticket.STATUS_CHOICES)

    class Meta:
        model = Ticket
        fields = ('title', 'description', 'priority', 'request_type', 'status')

class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)

class RegisterForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)
    default_group = forms.ChoiceField(choices=[('Defaultuser', 'Defaultuser')], widget=forms.HiddenInput, required=False)

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('hasla nie sa identyczne')
        return cd['password2']