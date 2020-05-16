from datetime import datetime

from accounts.models import Doctor, Client
from .models import Ticket



def validate_ticket(client_id, doctor_id, date, time):
	"""Validate ticket data
	   return: bool, string
	"""

	if not client_id or not doctor_id or not date or not time:
		return False, 'Not all data! You not selected a time for ticket.'

	date = datetime.strptime(date, '%Y-%m-%d')
	now_date = datetime.today()

	if date < now_date:
		return False, 'Wrong date! You selected a date earlier than possible date.'

	try:
		doctor_to = Doctor.objects.get(id=doctor_id)
		ticket = Ticket.objects.get(doctor_to=doctor_to, date=date, time=time)
		return False, 'Ticket for this doctor with such time already exists.'
	except:
		pass

	return True, ''