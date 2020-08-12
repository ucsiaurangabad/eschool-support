from django import forms
from .models import *

class ProfileImageForm(forms.ModelForm):
    class Meta:
	    model = ProfileImage
	    fields = '__all__'