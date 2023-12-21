from itertools import chain
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, User
from django.contrib.auth.views import LogoutView
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import Q


from .forms import AddTicketForm, EditTicketForm, LoginForm, RegisterForm
from .models import Ticket


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
    if request.user.groups.filter(name='Defaultuser').exists():
        tickets = Ticket.objects.filter(created_by=request.user)
    else:
        tickets = Ticket.objects.filter(Q(assigned_to=request.user) | Q(assigned_to=None))
    paginator = Paginator(tickets, 5)
    page = request.GET.get('page')
    paginator = Paginator(tickets, 5)
    page = request.GET.get('page')
    try:
        tickets = paginator.page(page)
    except PageNotAnInteger:
        tickets = paginator.page(1)
    except EmptyPage:
        tickets = paginator.page(paginator.num_pages)
    return render(request, 'helpdeskapp/tickets/ticket_list.html', {'page': page ,'tickets': tickets})


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
    ticket = get_object_or_404(Ticket, slug=slug)
    if request.method == "POST":
        form = EditTicketForm(request.POST, instance=ticket)
        if form.is_valid():
            ticket = form.save()
            return redirect('helpdeskapp:ticket_detail', slug=ticket.slug)
    else:
        form = EditTicketForm(instance=ticket)
    return render(request, 'helpdeskapp/tickets/ticket_edit.html', {'form': form})


def ticket_delete(request, slug):
    ticket = get_object_or_404(Ticket, slug=slug)
    ticket.delete()
    return redirect('helpdeskapp:ticket_list')

def assigned_to(request, slug):
    ticket = get_object_or_404(Ticket, slug=slug)
    if ticket.assigned_to:
        return HttpResponse('Zgłoszenie jest już przypisane')
    if request.user.groups.filter(name='Defaultuser').exists():
        return HttpResponse('Nie masz uprawnień do przypisania zgłoszenia')
    else:
        ticket.assigned_to = request.user
        ticket.save()
    return redirect('helpdeskapp:ticket_detail', slug=ticket.slug)

def main_view(request):
    return render(request, 'helpdeskapp/main.html')