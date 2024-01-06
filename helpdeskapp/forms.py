from django import forms
from django.contrib.auth.models import User
from helpdeskapp.models import Ticket


class AddTicketForm(forms.ModelForm):
    title = forms.CharField(max_length=100)
    description = forms.CharField(widget=forms.Textarea)
    priority = forms.ChoiceField(choices=Ticket.prioritylist)
    request_type = forms.ChoiceField(choices=Ticket.request_typelist)
    
    class Meta:
        model = Ticket
        fields = ('title', 'description', 'priority', 'request_type')

class EditTicketForm(forms.ModelForm):
    title = forms.CharField(max_length=100)
    description = forms.CharField(widget=forms.Textarea)
    priority = forms.ChoiceField(choices=Ticket.prioritylist)
    request_type = forms.ChoiceField(choices=Ticket.request_typelist)
    status = forms.ChoiceField(choices=Ticket.statuslist)

    class Meta:
        model = Ticket
        fields = ('title', 'description', 'priority', 'request_type', 'status')

class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)

class RegisterForm(forms.Form):
    username = forms.CharField(max_length=100)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)
    default_group = forms.ChoiceField(choices=[('Defaultuser', 'Defaultuser')], widget=forms.HiddenInput, required=False)

