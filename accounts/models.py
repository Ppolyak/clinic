from django.db import models
from django.contrib.auth.models import User


GENDER_CHOICES = (
    ('M', 'Male'),
    ('F', 'Female'),
)

class Department(models.Model):
	name = models.CharField(max_length=50, null=True, blank=True)

	def __str__(self):
		return self.name


class Client(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=False, blank=True)
	firstname = models.CharField(max_length=50, null=False, blank=True)
	lastname = models.CharField(max_length=50, null=False, blank=True)
	email = models.EmailField(null=True, blank=True)
	birth_date = models.DateField(null=True, blank=True)
	phone_number = models.CharField(max_length=15, null=True, blank=True)

	def __str__(self):
		return self.get_fullname()

	def get_fullname(self):
		return '{} {}'.format(self.firstname, self.lastname)


class Doctor(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=False, blank=True)
	firstname = models.CharField(max_length=50, null=False, blank=True)
	lastname = models.CharField(max_length=50, null=False, blank=True)
	email = models.EmailField(null=True, blank=True)
	department = models.ForeignKey(Department, null=True, on_delete=models.SET_NULL)
	birth_date = models.DateField(null=True, blank=True)
	schedule = models.CharField(max_length=50, null=True, blank=True)
	working_position = models.CharField(max_length=50, null=True, blank=True)
	experience = models.IntegerField(null=True, blank=True)
	clients = models.ManyToManyField(Client)
	phone_number = models.CharField(max_length=15, null=True, blank=True)

	def __str__(self):
		return self.get_fullname()

	def get_fullname(self):
		return '{} {}'.format(self.firstname, self.lastname)

