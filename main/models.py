from django.db import models

from accounts.models import Client, Doctor


STATUS_CHOICES = (
	('Waiting', 'Waiting'),
    ('Declined', 'Declined'),
    ('Approved', 'Approved'),
)

APPROVED_STATUS = 'Approved'
DECLINED_STATUS = 'Declined'
WAITING_STATUS = 'Waiting'

class Ticket(models.Model):
	client_from = models.ForeignKey(Client, null=True, on_delete=models.SET_NULL)
	doctor_to = models.ForeignKey(Doctor, null=True, on_delete=models.SET_NULL)
	date = models.DateField(null=True, blank=True)
	time = models.TimeField(null=True, blank=True)

	def __str__(self):
		return 'From: {} - To: {}. {} | {}'.format(self.client_from,
			self.doctor_to, self.date, self.time)


class Request(models.Model):
	client_from = models.ForeignKey(Client, null=True, on_delete=models.SET_NULL)
	doctor_to = models.ForeignKey(Doctor, null=True, on_delete=models.SET_NULL)
	status = models.CharField(max_length=15, choices=STATUS_CHOICES, default=WAITING_STATUS, null=True, blank=True)

	def __str__(self):
		return 'From: {} - To: {}. Status: {}'.format(self.client_from,
			self.doctor_to, self.status)