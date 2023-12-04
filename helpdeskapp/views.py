from calendar import day_abbr
from django.forms import SlugField
from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView

from helpdeskapp.models import Ticket
# Create your views here.
class TicketListView(ListView):
    queryset = Ticket.published.all()
    template_name = 'helpdeskapp/tickets/ticket_list.html'
    context_object_name = 'tickets'
    paginate_by = 5

def ticket_detail(request, slug):
    ticket = get_object_or_404(Ticket, slug=slug)
    return render(request, 'helpdeskapp/tickets/ticket_detail.html', {'ticket': ticket})