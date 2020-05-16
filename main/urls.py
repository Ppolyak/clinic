from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^$', views.home, name='home'),
	url(r'^doctors/', views.doctors, name='doctors'),
	url(r'^ajax/create_ticket/', views.create_ticket, name='create_ticket'),
	url(r'^ajax/send_request/', views.send_request, name='send_request'),
	url(r'^ajax/approve_request/', views.approve_request, name='approve_request'),
	url(r'^ajax/decline_request/', views.decline_request, name='decline_request'),
]