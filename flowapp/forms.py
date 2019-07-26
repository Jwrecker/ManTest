from django import forms
from django.db import models
from django.forms import ModelForm
from django.utils import timezone

from .models import StepType, Project, Flow, Step


class StepForm(forms.Form):
    step_type = forms.ModelChoiceField(queryset=StepType.objects.all())
    order = forms.IntegerField()
    item = forms.CharField(max_length=100)
    passed = forms.NullBooleanField()
    desired_result = forms.CharField(max_length=500)
    has_fixture = forms.NullBooleanField()
    fixture_name = forms.CharField(max_length=100)

#    class Meta:
#        model = Step
#        fields = ['step_type', 'flow', 'order', 'item', 'passed', 'desired_result', 'has_fixture', 'fixture_name']


"""
class DefaultStepForm(forms.Form):
    order = forms.IntegerField(defualt=1)
    flow = forms.ModelChoiceField(queryset=Flow.objects.all())
    desired_result = forms.CharField(max_length=500, blank=True, null=True)
    passed = forms.NullBooleanField()
    has_fixture = forms.NullBooleanField()
    fixture_name = forms.CharField(max_length=100, blank=True, null=True)
    item = forms.CharField(max_length=100, blank=True, null=True)


class NoValidateStepForm(forms.Form):
    order = forms.IntegerField(defualt=1)
    flow = forms.ModelChoiceField(queryset=Flow.objects.all())
    has_fixture = forms.NullBooleanField()
    fixture_name = forms.CharField(max_length=100, blank=True, null=True)
    item = forms.CharField(max_length=100, blank=True, null=True)


class MaybeURLStepForm(forms.Form):
    order = forms.IntegerField(defualt=1)
    flow = forms.ModelChoiceField(queryset=Flow.objects.all())
    desired_result = forms.CharField(max_length=500, null=True)
    passed = forms.BooleanField()
    has_fixture = forms.BooleanField()
    fixture_name = forms.CharField(max_length=100, null=True)
    item = forms.CharField(max_length=100, null=True)


class URLStepForm(forms.Form):
    order = forms.IntegerField(defualt=1)
    flow = forms.ModelChoiceField(queryset=Flow.objects.all())
    desired_result = forms.CharField(max_length=500, blank=True, null=True)
    passed = forms.NullBooleanField()
    has_fixture = forms.NullBooleanField()
    fixture_name = forms.CharField(max_length=100, blank=True, null=True)
    item = forms.URLField(max_length=100, null=True)


class ValidateStepForm(forms.Form):
    order = forms.IntegerField(defualt=1)
    flow = forms.ModelChoiceField(queryset=Flow.objects.all())
    desired_result = forms.CharField(max_length=500, null=True)
    passed = forms.BooleanField()
    has_fixture = forms.NullBooleanField()
    fixture_name = forms.CharField(max_length=100, blank=True, null=True)
    item = forms.URLField(max_length=100, blank=True, null=True)


class FixtureStepForm(forms.Form):
    order = forms.IntegerField(defualt=1)
    flow = forms.ModelChoiceField(queryset=Flow.objects.all())
    desired_result = forms.CharField(max_length=500, blank=True, null=True)
    passed = forms.NullBooleanField()
    has_fixture = forms.BooleanField()
    fixture_name = forms.CharField(max_length=100, null=True)
    item = forms.CharField(max_length=100, blank=True, null=True)


class RestrictedStepForm(forms.Form):
    order = forms.IntegerField(defualt=1)
    flow = forms.ModelChoiceField(queryset=Flow.objects.all())


class ValidateOnlyStepForm(forms.Form):
    order = forms.IntegerField(defualt=1)
    flow = forms.ModelChoiceField(queryset=Flow.objects.all())
    desired_result = forms.CharField(max_length=500, null=True)
    passed = forms.NullBooleanField()
    item = forms.CharField(max_length=100, blank=True, null=True)


class FixtureOnlyStepForm(forms.Form):
    order = forms.IntegerField(defualt=1)
    flow = forms.ModelChoiceField(queryset=Flow.objects.all())
    desired_result = forms.CharField(max_length=500, blank=True, null=True)
    passed = forms.NullBooleanField()
    has_fixture = forms.NullBooleanField()
    fixture_name = forms.CharField(max_length=100, blank=True, null=True)
    item = forms.CharField(max_length=100, blank=True, null=True)
"""


class FlowForm(forms.Form):
    project = forms.ModelChoiceField(queryset=Project.objects.all())
    name = forms.CharField(max_length=75)
    passed = forms.NullBooleanField()
    order = forms.IntegerField()


class ProjectForm(forms.Form):
    name = forms.CharField(max_length=50)


class StepTypeForm(forms.Form):
    step_type = forms.ModelChoiceField(queryset=StepType.objects.all())


class AddStepTypeForm(ModelForm):
    class Meta:
        model = StepType
        fields = ['name', 'url_validation', 'has_verification', 'has_fixture']
