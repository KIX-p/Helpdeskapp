from calendar import day_abbr
from django.forms import SlugField
from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView

from helpdeskapp.admin import TicketAdmin
from .forms import AddTicketForm   

from helpdeskapp.models import Ticket
from django.contrib.auth.models import User
# Create your views here.
class TicketListView(ListView):
    queryset = Ticket.published.all()
    template_name = 'helpdeskapp/tickets/ticket_list.html'
    context_object_name = 'tickets'
    paginate_by = 5


def ticket_detail(request, slug):
    ticket = get_object_or_404(Ticket, slug=slug)
    return render(request, 'helpdeskapp/tickets/ticket_detail.html', {'ticket': ticket})

def ticket_add(request):
    if request.method == 'POST':
        form = AddTicketForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.created_by = User.objects.first()
            form.save()
    else:
        form = AddTicketForm()
    return render(request, 'helpdeskapp/tickets/ticket_add.html', {'form': form})