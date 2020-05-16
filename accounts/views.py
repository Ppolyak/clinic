from django.shortcuts import render_to_response, redirect, render
from django.contrib import auth, messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.template.context_processors import csrf
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q

from main.models import Ticket, Request
from .forms import ClientForm
from .models import Client, Doctor
from .helper import get_user_role, parse_schedule, get_disabled_tickets


def login(request):
	"""Login user
	"""
	template_name = 'accounts/login.html'
	success_url = '/'
	success_mesage = 'You are logged successfully.'
	error_message = 'Incorrect login or password. Try again.'

	args = {}
	args.update(csrf(request))
	
	if request.POST:
		username = request.POST.get('username', '')
		password = request.POST.get('password', '')
		user = auth.authenticate(username=username, password=password)

		if user != None:
			auth.login(request, user)
			request.session['user_role'] = get_user_role(user)
			messages.add_message(request, messages.SUCCESS, success_mesage)
			return redirect(success_url)
		else:
			messages.add_message(request, messages.ERROR, error_message)
	return render(request, template_name, args)


def register(request):
	"""Register user
	"""
	template_name = 'accounts/register.html'
	success_url = '/accounts/login'
	success_mesage = 'You are registered successfully.'
	error_message = 'Incorrect data. Try again.'

	args = {}
	args.update(csrf(request))
	args['user_form'] = UserCreationForm()
	args['client_form'] = ClientForm()

	if request.POST:
		create_user_form = UserCreationForm(request.POST)
		create_client_form = ClientForm(request.POST)
		if create_user_form.is_valid() and create_client_form.is_valid():
			user = create_user_form.save(commit=False)
			client = create_client_form.save(commit=False)
			user.save()

			#add user to client and save
			client.user = user
			client.save()
			
			user = auth.authenticate(
				username=create_user_form.cleaned_data['username'],
				password=create_user_form.cleaned_data['password1'])
			messages.add_message(request, messages.SUCCESS, success_mesage)
			return redirect(success_url)
		else:
			args['user_form'] = create_user_form
			args['client_form'] = create_client_form
			messages.add_message(request, messages.ERROR, error_message)
	return render(request, template_name, {'user_form': args['user_form'],
										   'client_form': args['client_form']})


@login_required(login_url='/')
def update_profile(request):
	"""Update profile information
	"""
	template_name = 'accounts/update.html'
	success_url = '/accounts/profile'
	success_mesage = 'Your account was updated successfully.'
	error_message = 'Incorrect data. Your account was not updated.'

	client_form = ClientForm(request.POST, instance=request.user.client)

	if request.method == 'POST':
		client_form = ClientForm(request.POST, instance=request.user.client)
		if client_form.is_valid():
			client_form.save()
			messages.add_message(request, messages.SUCCESS, success_mesage)
			return redirect(success_url)
		else:
			messages.add_message(request, messages.ERROR, error_message)
	else:
		client_form = ClientForm(instance=request.user.client)
	
	return render(request, template_name, {'client_form': client_form})


@login_required(login_url='/')
def view_profile(request):
	"""View self profile
	"""
	template_name_client = 'accounts/client_profile.html'
	template_name_doctor = 'accounts/doctor_profile.html'
	
	user = request.user
	user_role = request.session['user_role']

	if user_role == 'client':
		profile = user.client
		doctors = profile.doctor_set.all()
		tickets = profile.ticket_set.all().order_by('date')
		return render(request, template_name_client, {'profile': profile,
													  'doctors': doctors,
													  'tickets': tickets})
	else:
		profile = user.doctor
		clients = profile.clients.all()
		requests = profile.request_set.all()
		tickets = profile.ticket_set.all().order_by('date')
		return render(request, template_name_doctor, {'profile': profile,
													  'clients': clients,
													  'requests': requests,
													  'tickets': tickets})


@login_required(login_url='/')
def logout(request):
	"""Logout user
	"""
	success_url = '/'
	success_mesage = 'You are logout successfully';

	try:
		del request.session['user_role']
	except:
		pass
	auth.logout(request)
	messages.add_message(request, messages.SUCCESS, success_mesage);
	
	return redirect(success_url)


def view_doctor(request, id):
	"""View doctor profile
	"""
	template_name = 'accounts/doctor.html'

	doctor = Doctor.objects.get(id=id)
	tickets = doctor.ticket_set.all()
	client = Client.objects.get(user=request.user)

	criteria_d = Q(doctor_to=doctor)
	criteria_c = Q(client_from=client)
	client_tickets = tickets.filter(criteria_d & criteria_c)
	try:
		client_request = Request.objects.get(criteria_d & criteria_c)
	except ObjectDoesNotExist:
		client_request = None

	is_added_doctor = client in doctor.clients.all()

	disabled_days, time_intervals = parse_schedule(doctor.schedule)
	disabled_tickets = get_disabled_tickets(tickets)

	return render(request, template_name, {'doctor': doctor,
										   'client': client,
										   'is_added_doctor': is_added_doctor,
										   'client_request': client_request,
										   'client_tickets': client_tickets,
										   'disabled_days': disabled_days,
										   'time_intervals': time_intervals})