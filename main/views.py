from django.shortcuts import render
from django.http import JsonResponse

from accounts.models import Client, Doctor
from .models import Ticket, Request, APPROVED_STATUS, DECLINED_STATUS, WAITING_STATUS
from .validators import validate_ticket


def home(request):
	"""Return home page
	"""
	template_name = 'main/home.html'
	return render(request, template_name)


def doctors(request):
	"""Return page with all doctors
	"""
	template_name = 'main/doctors.html'

	doctors = Doctor.objects.all()

	return render(request, template_name, {'doctors': doctors})


def create_ticket(request):
	"""Create ticket from client to doctor
	   return: JsonResponse
	"""
	if request.GET:
		client_id = request.GET.get('client_id', '')
		doctor_id = request.GET.get('doctor_id', '')
		date = request.GET.get('date', '')
		time = request.GET.get('time', '')

	ticket_is_valid, message = validate_ticket(client_id, doctor_id, date, time)
	if ticket_is_valid == False:
		data = {
			'success': False,
			'message': message
		}
		response = JsonResponse(data)
		response.status_code = 403
		return response

	client = Client.objects.get(id=client_id)
	doctor = Doctor.objects.get(id=doctor_id)

	ticket = Ticket(client_from=client, doctor_to=doctor, time=time, date=date)
	ticket.save()

	data = {
		'success': True,
		'message': message
	}
	response = JsonResponse(data)

	return response


def send_request(request):
	"""Send request for addind from client to doctor
	   return: JsonResponse
	"""
	if request.GET:
		client_id = request.GET.get('client_id', '')
		doctor_id = request.GET.get('doctor_id', '')

	client = Client.objects.get(id=client_id)
	doctor = Doctor.objects.get(id=doctor_id)

	request = Request(client_from=client, doctor_to=doctor)
	request.save()

	data = {}
	response = JsonResponse(data)

	return response


def approve_request(request):
	"""Change request status on approved
	   return JsonResponse
	"""
	if request.GET:
		request_id = request.GET.get('request_id', '')

	request = Request.objects.get(id=request_id)
	request.status = APPROVED_STATUS
	request.save()

	client = request.client_from
	doctor = request.doctor_to
	doctor.clients.add(client)
	doctor.save()

	data = {}
	response = JsonResponse(data)

	return response


def decline_request(request):
	"""Change request status on declined
	   return JsonResponse
	"""
	if request.GET:
		request_id = request.GET.get('request_id', '')

	request = Request.objects.get(id=request_id)
	request.update(status=DECLINED_STATUS)
	
	data = {}
	response = JsonResponse(data)

	return response