from calendar import day_abbr
from imaplib import _Authenticator
from django.forms import SlugField
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView

from helpdeskapp.admin import TicketAdmin
from .forms import AddTicketForm, LoginForm 

from django.contrib.auth import authenticate, login
from django.http import HttpResponse


from helpdeskapp.models import Ticket
from django.contrib.auth.models import User

from django.contrib.auth.views import LoginView

from django.contrib.auth.views import LogoutView
from django.urls import reverse_lazy

from django.contrib.auth.decorators import login_required

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# Create your views here.

"""
    View function for user login.

    This function handles the login form submission and authenticates the user.
    If the user is authenticated and active, it logs them in and redirects to the ticket list page.
    If the user is authenticated but not active, it returns an HttpResponse indicating that the account is blocked.
    If the user is not authenticated, it returns an HttpResponse indicating that the credentials are invalid.

    :param request: The HTTP request object.
    :return: The HTTP response object.
    """
def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])

            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('helpdeskapp:ticket_list')
                else:
                    return HttpResponse('konto jest zablokowane')
            else:
                return HttpResponse('Nieprawidlowe dane uwierzytelniajace')
    else:
        form = LoginForm()
    return render(request, 'helpdeskapp/registration/login.html', {'form': form})



class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('helpdeskapp:login')

@login_required
def ticket_list(request):
    tickets = Ticket.published.all()
    paginator = Paginator(tickets, 5)
    page = request.GET.get('page')
    try:
        tickets = paginator.page(page)
    except PageNotAnInteger:
        tickets = paginator.page(1)
    except EmptyPage:
        tickets = paginator.page(paginator.num_pages)
    return render(request, 'helpdeskapp/tickets/ticket_list.html', {'page': page, 'tickets': tickets})


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


    