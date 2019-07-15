from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.views import generic
from django.utils import timezone
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from rest_framework import viewsets
# from .serializers import UserSerializer, GroupSerializer

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


@require_POST
def MoveStep(request):

    pk = request.pk
    order = request.order

    s = Step.objects.get(pk=pk)
    print(s)

    Step.objects.move(obj = s, new_order = order)

    return HttpResponse("That seemed to work.")

# class UserViewSet(viewsets.ModelViewSet):
    # queryset = User.objects.all().order_by('date_joined')
    # serializer_class = UserSerializer


# class GroupViewSet(viewsets.ModelViewSet):
  # queryset = Group.objects.all()
   # serializer_class = GroupSerializer
