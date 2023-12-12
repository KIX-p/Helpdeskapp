from calendar import day_abbr
from imaplib import _Authenticator
from django.forms import SlugField, ValidationError
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView

from helpdeskapp.admin import TicketAdmin
from .forms import AddTicketForm, EditTicketForm, LoginForm, RegisterForm 

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

from django.contrib.auth.models import User, Group
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect, get_object_or_404
from .forms import EditTicketForm
from .models import Ticket

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            if User.objects.filter(username=cd['username']).exists():
                form.add_error('username', ValidationError("Nazwa użytkownika jest już zajęta."))
            else:
                user = User.objects.create_user(cd['username'], None, cd['password'])
                default_group = Group.objects.get(name='Defaultuser')
                user.groups.add(default_group)
                user.save()
                return redirect('helpdeskapp:login')
    else:
        form = RegisterForm()
    return render(request, 'helpdeskapp/registration/register.html', {'form': form})

@login_required
def ticket_list(request):
    tickets = Ticket.objects.all()
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
            ticket.created_by = request.user
            form.save()
            return redirect('helpdeskapp:ticket_list')  
    else:
        form = AddTicketForm()
    return render(request, 'helpdeskapp/tickets/ticket_add.html', {'form': form})

def ticket_edit(request, slug):
    # Pobieramy ticket na podstawie sluga, jeśli nie istnieje, zwracamy stronę 404
    ticket = get_object_or_404(Ticket, slug=slug)

    # Sprawdzamy, czy metoda żądania to POST
    if request.method == "POST":
        # Tworzymy instancję formularza z danymi przesłanymi w żądaniu POST
        form = EditTicketForm(request.POST, instance=ticket)

        # Sprawdzamy, czy formularz jest prawidłowy
        if form.is_valid():
            # Zapisujemy zmiany w tickecie do bazy danych
            ticket = form.save()

            # Przekierowujemy użytkownika do strony szczegółów ticketu
            return redirect('helpdeskapp:ticket_detail', slug=ticket.slug)
    else:
        # Jeśli metoda żądania to nie POST, tworzymy instancję formularza bez danych żądania POST
        form = EditTicketForm(instance=ticket)

    # Renderujemy szablon 'helpdeskapp/tickets/ticket_edit.html' z kontekstem, który zawiera formularz
    return render(request, 'helpdeskapp/tickets/ticket_edit.html', {'form': form})

def main_view(request):
    return render(request, 'helpdeskapp/main.html')



    