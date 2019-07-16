from django import forms
from django.db import models
from django.forms import ModelForm
from django.utils import timezone

from .models import Project, Flow, Step, StepType


class StepForm(forms.Form):
    pk = forms.IntegerField()
    order = forms.IntegerField()
