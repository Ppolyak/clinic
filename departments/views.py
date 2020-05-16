from django.shortcuts import render

from accounts.models import Department, Doctor

def departments(request):
	template_name = 'departments/departments.html'
	departments = Department.objects.all()

	return render(request, template_name, {'departments': departments})


def department_details(request, pk):
	template_name = 'departments/department_details.html'
	department = Department.objects.get(pk=pk)
	doctors = Doctor.objects.filter(department=department)

	return render(request, template_name, {'department': department, 'doctors': doctors})