from django.contrib import admin
from .models import Client, Doctor, Department


admin.site.register(Client)
admin.site.register(Doctor)
admin.site.register(Department)
