from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.views import generic
from django.utils import timezone
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt, requires_csrf_token
from rest_framework import viewsets
# from .serializers import UserSerializer, GroupSerializer

from .models import Project, Flow, Step, StepType


class ProjectListView(generic.ListView):
    """
    A view to list all projects
    """
    template_name = 'flowapp/index.html'
    context_object_name = 'main'
    model = Project

    def get_queryset(self):
        return Project.objects.all()


class ProjectDetailView(generic.DetailView):
    """
    A project detail view
    """
    template_name = 'flowapp/flow_list.html'
    model = Project


@require_POST
def move_step(request):
    """
    A view to move a step
    """
    old_flow_id = request.POST["old_flow"]
    new_flow_id = request.POST["new_flow"]
    pk = request.POST["step_pk"]
    order = int(request.POST["new_list_position"])
    # Check to see whether the step's flow has changed
    if old_flow_id == new_flow_id:
        # The step moved position within a flow
        s = Step.objects.get(pk=pk)
        project = s.flow.project.id
        Step.objects.move(obj=s, new_order=order)
        return HttpResponseRedirect('')

    else:
        # The step moved between flows
        s = Step.objects.get(pk=pk)
        f = Flow.objects.get(pk=new_flow_id)
#        n = Step.objects.create(
#            flow=f,
#            id=s.id,
#            step_type=s.step_type,
#            desired_result=s.desired_result,
#            passed=s.passed,
#            has_fixture=s.has_fixture,
#            fixture_name=s.fixture_name,
#            item=s.item
#        )
        # Find counts of Flows
        old_flow_count = Step.objects.filter(flow=s.flow).count()
        new_flow_count = Step.objects.filter(flow=f).count()
        # TODO: Something is breaking, fix it (IN THE PROCESS OF MOVING SOME OF THIS LOGIC TO THE MANAGER)
        # Copy step from old flow and put it at the end of the new flow
        # (There's some magic happening here by setting the pk to None)
        # See
        new_step = s
        new_step.flow = f
        new_step.pk = None
        new_step.order = new_flow_count+1
        new_step.save()
        # Then move it to the desired position within that new flow
        Step.objects.move(new_step, order)
        # Now delete the old step by moving it to the end of it's flow (to adjust the order of the remaining items)
        # ... then removing it.
        last_position = old_flow_count + 1
        Step.objects.move(s, last_position)
        Step.objects.remove(s)

        return HttpResponseRedirect('')


# class UserViewSet(viewsets.ModelViewSet):
    # queryset = User.objects.all().order_by('date_joined')
    # serializer_class = UserSerializer


# class GroupViewSet(viewsets.ModelViewSet):
  # queryset = Group.objects.all()
   # serializer_class = GroupSerializer
