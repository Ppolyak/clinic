from django import forms
from django.contrib.auth.models import User

from .models import Client

class ClientForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
    	super().__init__(*args, **kwargs)

    	for field in self.Meta.fields:
    		self.fields[field].required = True

    class Meta:
        model = Client
        fields = (
            'gender',
        	'firstname',
        	'lastname',
        	'email',
        	'birth_date',
            'phone_number',
        )
        widgets = {
        	'birth_date' : forms.DateInput(attrs={'class' : 'date_picker'})
        }
