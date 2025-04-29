from django.forms import ModelForm
from .models import *

class RegForm(ModelForm):
    class Meta:
        model = Player
        fields = '__all__'