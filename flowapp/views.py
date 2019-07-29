import json
from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.views import generic
from django.utils import timezone
from django.urls import reverse
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt, requires_csrf_token
from rest_framework import viewsets
from django import forms

# from .serializers import UserSerializer, GroupSerializer
from .forms import *

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

    def get_context_data(self, **kwargs):
        context = super(ProjectListView, self).get_context_data(**kwargs)
        context['step_types'] = StepType.objects.all()
        return context


class ProjectDetailView(generic.DetailView):
    """
    A project detail view
    """
    template_name = 'flowapp/flow_list.html'
    model = Project

    def get_context_data(self, **kwargs):
        context = super(ProjectDetailView, self).get_context_data(**kwargs)
        context['step_types'] = StepType.objects.all()
        return context


@require_POST
def move_step(request):
    """
    A view to move a step
    """
    old_flow_id = request.POST["old_flow"]
    new_flow_id = request.POST["new_flow"]
    pk = request.POST["step_pk"]
    order = int(request.POST["new_list_position"])
    old_flow = Flow.objects.get(pk=old_flow_id)
    new_flow = Flow.objects.get(pk=new_flow_id)
    s = Step.objects.get(pk=pk)
    Step.objects.move(obj=s, new_order=order, source_flow=old_flow, target_flow=new_flow)
    json_data = {"old_flow_id": old_flow_id, "new_flow_id": new_flow_id}
    return JsonResponse(json_data)

#def get_step_type(request):
#    if request.method == 'POST':
#
#        form = StepTypeForm
#
#        if form.is_valid():
#            step_type = form.cleaned_data['step_type']
        # TODO: Either have step_type in the form, and validate after to see if they did it correctly, or load a second form.


class StepFormBuilder():
    """
    Builds forms based of a given step type.
    """
    def build_form(self):
        class StepForm(forms.Form):
            step_type = self
            order = forms.IntegerField()
            flow = forms.ModelChoiceField(queryset=Flow.objects.all())
            if step_type.has_verification == "A":
                passed = forms.NullBooleanField()
                desired_result = forms.CharField(max_length=500, required=False)
            elif step_type.has_verification == "R":
                passed = forms.BooleanField()
                desired_result = forms.CharField(max_length=500, required=True)
            else:
                pass
            if step_type.has_fixture == "A":
                has_fixture = forms.NullBooleanField()
                fixture_name = forms.CharField(max_length=100, required=False)
            elif step_type.has_fixture == "R":
                has_fixture = forms.BooleanField()
                fixture_name = forms.CharField(max_length=100)
            else:
                pass
            if step_type.url_validation == "A":
                item = forms.URLField(max_length=200, required=False)
            elif step_type.url_validation == "R":
                item = forms.URLField(max_length=200, required=True)
            else:
                item = forms.CharField(max_length=200, required=False)

        return StepForm()


def get_step_form(request):
    if request.method == 'POST':
        step_type_id = request.POST.get("step_type_id")
        print(step_type_id)
        form = StepForm(step_type_id=step_type_id)
        return render(request, 'flowapp/test_forms.html', {'form': form})


def add_step(request):
    if request.method == 'POST':
        step_type_id = request.POST.get("step_type_id")
        print(step_type_id)
        form = StepForm(step_type_id=step_type_id)
        print(form)

        if form.is_valid():
            desired_result = form.cleaned_data['desired_result']
            has_fixture = form.cleaned_data['has_fixture']
            fixture_name = form.cleaned_data['fixture_name']
            passed = form.cleaned_data['passed']
            item = form.cleaned_data['item']
            flow = form.cleaned_data['flow']StepFormBuilder.build_form(step_type)
            step_type = StepType.objects.get(pk=step_type_id)
            step = Step.objects.create(flow=flow,
                                       step_type=step_type,
                                       desired_result=desired_result,
                                       has_fixture=has_fixture,
                                       fixture_name=fixture_name,
                                       passed=passed,
                                       item=item
                                       )
            step.save()
            return HttpResponseRedirect('/project/')
        else:
            form = StepForm(step_type_id=step_type_id)
        return render(request, 'flowapp/flow_list.html', {'form': form})



                #    else:
#        s = Step.objects.get(pk=pk)
#        f = Flow.objects.get(pk=new_flow_id)
#        n = Step.objects.create(
#                    flow=f,
#                    id=s.id,
#                    step_type=s.step_type,
#                    desired_result=s.desired_result,
#                    passed=s.passed,
#                    has_fixture=s.has_fixture,
#                    fixture_name=s.fixture_name,
#                    item=s.item
#                )
#        Step.objects.move(n, order)
#        flow_count = Step.objects.filter(flow=s.flow).count()
#        Step.objects.move(s, flow_count+1)
#        Step.objects.remove(s)
#        return HttpResponseRedirect('')
    # The step moved between flows
    # s = Step.objects.get(pk=pk)
    # f = Flow.objects.get(pk=new_flow_id)
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
    #old_flow_count = Step.objects.filter(flow=s.flow).count()
    #new_flow_count = Step.objects.filter(flow=f).count()
    # TODO: Something is breaking, fix it (IN THE PROCESS OF MOVING SOME OF THIS LOGIC TO THE MANAGER)
    # Copy step from old flow and put it at the end of the new flow
    # (There's some magic happening here by setting the pk to None)
    # See
    # new_step = s
    # new_step.flow = f
    # new_step.pk = None
    # new_step.order = new_flow_count+1
    # new_step.save()
    # Then move it to the desired position within that new flow
    # Step.objects.move(new_step, order)
    # Now delete the old step by moving it to the end of it's flow (to adjust the order of the remaining items)
    # ... then removing it.
    # last_position = old_flow_count + 1
    # Step.objects.move(s, last_position)
    # Step.objects.remove(s)


# class UserViewSet(viewsets.ModelViewSet):
    # queryset = User.objects.all().order_by('date_joined')
    # serializer_class = UserSerializer


# class GroupViewSet(viewsets.ModelViewSet):
  # queryset = Group.objects.all()
   # serializer_class = GroupSerializer
""" if step_type.url_validation == 'A' and step_type.has_fixture == 'A' and step_type.has_validation == 'A':
                s_form = DefaultStepForm

            elif step_type.url_validation == 'A' and step_type.has_fixture == 'A' and step_type.has_validation == 'R':
                s_form = ValidateStepForm

            elif step_type.url_validation == 'A' and step_type.has_fixture == 'A' and step_type.has_validation == 'D':
                s_form = NoValidateStepForm

            elif step_type.url_validation == 'A' and step_type.has_fixture == 'R' and step_type.has_validation == 'A':
                s_form = FixtureStepForm

            elif step_type.url_validation == 'A' and step_type.has_fixture == 'R' and step_type.has_validation == 'R':
                s_form = MaybeURLStepForm

            elif step_type.url_validation == 'A' and step_type.has_fixture == 'R' and step_type.has_validation == 'D':
                s_form =

            elif step_type.url_validation == 'A' and step_type.has_fixture == 'D' and step_type.has_validation == 'A':
                s_form =

            elif step_type.url_validation == 'A' and step_type.has_fixture == 'D' and step_type.has_validation == 'R':
                s_form =

            elif step_type.url_validation == 'A' and step_type.has_fixture == 'D' and step_type.has_validation == 'D':
                s_form =

            elif step_type.url_validation == 'R' and step_type.has_fixture == 'A' and step_type.has_validation == 'A':
                s_form =

            elif step_type.url_validation == 'R' and step_type.has_fixture == 'A' and step_type.has_validation == 'R':
                s_form =

            elif step_type.url_validation == 'R' and step_type.has_fixture == 'A' and step_type.has_validation == 'D':
                s_form =

            elif step_type.url_validation == 'R' and step_type.has_fixture == 'R' and step_type.has_validation == 'A':
                s_form =

            elif step_type.url_validation == 'R' and step_type.has_fixture == 'R' and step_type.has_validation == 'R':
                s_form =

            elif step_type.url_validation == 'R' and step_type.has_fixture == 'R' and step_type.has_validation == 'D':
                s_form =

            elif step_type.url_validation == 'R' and step_type.has_fixture == 'D' and step_type.has_validation == 'A':
                s_form =

            elif step_type.url_validation == 'R' and step_type.has_fixture == 'D' and step_type.has_validation == 'R':
                s_form =

            elif step_type.url_validation == 'R' and step_type.has_fixture == 'D' and step_type.has_validation == 'D':
                s_form =

            elif step_type.url_validation == 'D' and step_type.has_fixture == 'A' and step_type.has_validation == 'A':
                s_form = DefaultStepForm

            elif step_type.url_validation == 'D' and step_type.has_fixture == 'A' and step_type.has_validation == 'R':
                s_form =

            elif step_type.url_validation == 'D' and step_type.has_fixture == 'A' and step_type.has_validation == 'D':
                s_form =

            elif step_type.url_validation == 'D' and step_type.has_fixture == 'R' and step_type.has_validation == 'A':
                s_form =

            elif step_type.url_validation == 'D' and step_type.has_fixture == 'R' and step_type.has_validation == 'R':
                s_form =

            elif step_type.url_validation == 'D' and step_type.has_fixture == 'R' and step_type.has_validation == 'D':
                s_form = FixtureOnlyStepForm

            elif step_type.url_validation == 'D' and step_type.has_fixture == 'D' and step_type.has_validation == 'A':
                s_form =

            elif step_type.url_validation == 'D' and step_type.has_fixture == 'D' and step_type.has_validation == 'R':
                s_form = ValidateOnlyStepForm

            elif step_type.url_validation == 'D' and step_type.has_fixture == 'D' and step_type.has_validation == 'D':
                s_form ="""