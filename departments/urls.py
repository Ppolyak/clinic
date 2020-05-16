from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^$', views.departments, name='departments'),
	url(r'^(?P<pk>\d+)$', views.department_details, name='department_details'),
]