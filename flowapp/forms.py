from django import forms
from django.db import models
from django.forms import ModelForm
from django.utils import timezone

from .models import StepType, Project, Flow, Step


#class StepForm(forms.Form):
#    pk = forms.IntegerField()
#    order = forms.IntegerField()