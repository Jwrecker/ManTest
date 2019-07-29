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


class TestFormView(generic.ListView):
    """
    A view to test how the forms render
    """
    template_name = 'flowapp/test_forms.html'
    model = StepType
    context_object_name = 'step_type_list'

    def get_queryset(self):
        return StepType.objects.all()


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



def get_step_forms(request):
    step_type_id = request.POST.get("step_type_id")
    print(step_type_id)
    form = StepForm(step_type_id=step_type_id)
    return render(request, 'flowapp/test_forms.html', {'form': form, 'step_type_id': step_type_id})


def test_step_forms(request):
#    context = {}
#    forms = []
#    for st in StepType.objects.all():
#        forms.append(StepForm(step_type_id=st.pk))
#    context['forms'] = forms
#    return render(request, 'flowapp/test_forms.html', context)

    context = {}
    step_types = StepType.objects.all()
    context['step_types'] = step_types
    return render(request, 'flowapp/test_forms.html', context)


def step_form(request):
    step_type_id = request.POST.get("step_type_id")
    print(step_type_id)

    if request.method == 'POST':
        #action = request.POST.get("action")
        #if action == "create":
        form = StepForm(step_type_id, request.POST)
        if form.is_valid():
            desired_result = form.cleaned_data['desired_result']
            fixture = form.cleaned_data['fixture']
            passed = form.cleaned_data['passed']
            url = form.cleaned_data['url']
            flow = form.cleaned_data['flow']
            # step_type = StepType.objects.get(pk=step_type_id)
            step = Step.objects.create(flow=flow,
                                       desired_result=desired_result,
                                       fixture=fixture,
                                       passed=passed,
                                       url=url
                                       )
            step.save()
            return HttpResponse("Cool")
        else:
            form = StepForm(step_type_id=step_type_id)
            return HttpResponse(form.as_p())
    else:
        return render(request, 'flowapp/test_forms.html', {'form': form})



def add_step(request):
    if request.method == 'POST':
        step_type_id = request.POST.get("step_type_id")
        print(step_type_id)
        form = StepForm(request.POST)
        print(form)

        if form.is_valid():
            desired_result = form.cleaned_data['desired_result']
            fixture = form.cleaned_data['fixture']
            passed = form.cleaned_data['passed']
            url = form.cleaned_data['url']
            flow = form.cleaned_data['flow']
            # step_type = StepType.objects.get(pk=step_type_id)
            step = Step.objects.create(flow=flow,
                                       desired_result=desired_result,
                                       fixture=fixture,
                                       passed=passed,
                                       url=url
                                       )
            step.save()
            return HttpResponse("Cool")
        else:
            form = StepForm(step_type_id=step_type_id)
        return render(request, 'flowapp/test_forms.html', {'form': form})



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
#                    fixture=s.fixture,
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
#            fixture=s.fixture,
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