from datetime import datetime
from django.forms import SlugField
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from helpdeskapp.models import Ticket


# Create your views here.

@login_required
def chat_room(request, slug):
    ticket = get_object_or_404(Ticket, slug=slug)
    if not ticket.assigned_to:
        messages.warning(request, 'Nie możesz wejść do czatu, ponieważ nie został on jeszcze przydzielony.')
        return redirect('helpdeskapp:ticket_detail', slug=slug)
    return render(request, 'chat/room.html', {'ticket': ticket, 'slug': slug, 'username': request.user})
 

