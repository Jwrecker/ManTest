from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.views import generic
from django.utils import timezone
from django.urls import reverse
from django.http import HttpResponseRedirect

from .models import Project, Flow, Step, StepType


class IndexView(generic.ListView):

    template_name = 'flowapp/index.html'
    context_object_name = 'main'
    model = Project

    def get_queryset(self):
        return Project.objects.all()


class ProjectView(generic.DetailView):

    template_name = 'flowapp/flow_list.html'
    model = Project
