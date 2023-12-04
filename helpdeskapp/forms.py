from django import forms

from helpdeskapp.models import Ticket


class AddTicketForm(forms.ModelForm):
    title = forms.CharField(max_length=100)
    description = forms.CharField(widget=forms.Textarea)
    priority = forms.ChoiceField(choices=Ticket.STATUS_CHOICES2)
    request_type = forms.ChoiceField(choices=Ticket.STATUS_CHOICES3)
    status = forms.ChoiceField(choices=Ticket.STATUS_CHOICES)
    created_by = forms.CharField(max_length=100)

    class Meta:
        model = Ticket
        fields = ('title', 'description', 'priority', 'request_type', 'status')

