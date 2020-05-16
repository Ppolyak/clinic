from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^login/', views.login, name='login'),
	url(r'^logout/', views.logout, name='logout'),
	url(r'^register/', views.register, name='register'),
	url(r'^update/', views.update_profile, name='update'),
	url(r'^profile/', views.view_profile, name='profile'),
	url(r'^doctor/(?P<id>\d+)', views.view_doctor, name='doctor'),
]