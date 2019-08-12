import json
from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.views import generic
from django.utils import timezone
from django.urls import reverse
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt, requires_csrf_token
from rest_framework import viewsets
from django import forms
from django.core import serializers

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
    print(Flow.objects.all())
    order = int(request.POST["new_list_position"])
    old_flow = Flow.objects.get(pk=old_flow_id)
    new_flow = Flow.objects.get(pk=new_flow_id)
    s = Step.objects.get(pk=pk)
    Step.objects.move(obj=s, new_order=order, source_flow=old_flow, target_flow=new_flow)
    json_data = {"old_flow_id": old_flow_id, "new_flow_id": new_flow_id}
    return JsonResponse(json_data)

@require_POST
def move_flow(request):
    flow_id = request.POST['flow_id']
    direction = request.POST['direction']
    flow = Flow.objects.get(pk=flow_id)
    if direction == "up":
        order = flow.order - 1
        Flow.objects.move(flow, order)
    elif direction == "down":
        order = flow.order + 1
        Flow.objects.move(flow, order)
    else:
        raise IncorrectDirectionError
    return HttpResponse(flow.project.id)


def project_form(request):
    if request.method == "POST":
        name = request.POST.get('name')
        form = ProjectForm(request.POST)

        if form.is_valid():
            p = Project(name=name)
            p.save()
            return HttpResponse('Cool')
        else:
            return render(request, 'flowapp/project_form.html', {'form': form, 'status': "Failed"})

    else:
        form = ProjectForm()
        return render(request, 'flowapp/project_form.html', {'form': form})


def get_steps(request):
    step_id = request.GET.get("step_id")
    step = Step.objects.get(pk=step_id)
    flow = step.flow
    for st in flow.step_set.all():
        return render(request, 'flowapp/get_step.html', {'step': st})


def get_flows(request):
    project_id = request.GET.get("project_id")
    project = Project.objects.get(pk=project_id)
    step_types = StepType.objects.all()
    return render(request, 'flowapp/flows.html', {'project': project, 'step_types': step_types})


def get_flow(request):
    flow_id = request.GET.get("flow_id")
    flow = Flow.objects.get(pk=flow_id)
    return render(request, 'flowapp/get_flow.html', {'flow': flow})


def test_step_forms(request):
    if request.method == "POST":
        data = request.POST
        print(data)
    context = {}
    forms = []
    for st in StepType.objects.all():
        forms.append(StepForm(step_type_id=st.pk))
    context['forms'] = forms
#    return render(request, 'flowapp/test_forms.html', context)

#    context = {}
    context['step_types'] = StepType.objects.all()
    return render(request, 'flowapp/test_forms.html', context)


@require_POST
def delete_step(request):
    step_id = request.POST['step_id']
    step = Step.objects.get(pk=step_id)
    Step.objects.remove(step)
    return HttpResponse(step.flow.id)


def edit_step(request):

    if request.method == 'POST':
        step_id = request.POST.get("step_id")
        print(step_id)
        step = Step.objects.get(id=step_id)
        order = step.order
        flow = step.flow
        step_type = step.step_type
        step_type_id = step.step_type.id
        url = request.POST.get("url")
        passed = request.POST.get("passed")
        if passed == 'false':
            passed = False
        elif passed == 'true':
            passed = True
        else:
            passed = None
        desired_result = request.POST.get("desired_result")
        fixture = request.POST.get("fixture")
        form = StepForm(step_type_id, request.POST)
        if form.is_valid():
            Step.objects.remove(step)
            step = Step.objects.create(flow=flow,
                                       step_type=step_type,
                                       desired_result=desired_result,
                                       fixture=fixture,
                                       passed=passed,
                                       url=url
                                       )
            Step.objects.move(step, order, flow, flow)
            return HttpResponse(flow.id)
        else:
            json_data = {"form": str(form.as_p()), "status": "Failed"}
            return JsonResponse(json_data)
    else:
        step_id = request.GET.get('step_id')
        step = Step.objects.get(pk=step_id)
        step_type_id = step.step_type.id
        form = StepForm(step_type_id, initial={'flow': step.flow,
                                               'desired_result': step.desired_result,
                                               'fixture': step.fixture,
                                               'passed': step.passed,
                                               'url': step.url})
        form = form.as_p()
        return HttpResponse(form)


def step_form(request):

    if request.method == 'POST':
        print(request.POST)
        formdata = request.POST
        print(formdata)

        step_type_id = request.POST.get('step_type_id')
        step_type = StepType.objects.get(pk=step_type_id)
        flow_id = request.POST.get("flow")

        # if flow_id is None:
        #     raise FlowRequiredError
        flow = Flow.objects.get(pk=flow_id)
        order = request.POST.get("order")
        url = request.POST.get("url")
        # if step_type.url_validation == "R" and url is None:
        #     raise URLRequiredError
        # if url:

        passed = request.POST.get("passed")
        if passed == 'false':
            passed = False
        elif passed == 'true':
            passed = True
        else:
            passed = None
        print(passed)
        desired_result = request.POST.get("desired_result")
        fixture = request.POST.get("fixture")
        form = StepForm(step_type_id, request.POST)
        print(form)

        if form.is_valid():
            Step.objects.create(flow=flow,
                                step_type=step_type,
                                desired_result=desired_result,
                                fixture=fixture,
                                passed=passed,
                                url=url
                                )

        #
        #
        # #action = request.POST.get("action")
        # #if action == "create":
        #
        # form = StepForm(step_type_id)
        # if form.is_valid():
        #  # desired_result = form.cleaned_data['desired_result']
        #   #  fixture = form.cleaned_data['fixture']
        #    # passed = form.cleaned_data['passed']
        #    # url = form.cleaned_data['url']
        #    # flow = form.cleaned_data['flow']
        #    # # step_type = StepType.objects.get(pk=step_type_id)
        #
        #     step = Step.objects.create(flow=flow,
        #                                step_type=step_type,
        #                                desired_result=desired_result,
        #                                fixture=fixture,
        #                                passed=passed,
        #                                url=url
        #                                )
        #     step.save()
            print("Cool")
            return HttpResponse(flow.id)
        else:
            print("++++++++++++++++++++++++++++++++++++++++FORM FAILED VALIDATION======================================================")
            print(form)
            # return render(request, 'flowapp/step_form.html', {'form': form, 'status': "Failed"})
            json_data = {"form": str(form.as_p()), "status": "Failed"}
            return JsonResponse(json_data)
    else:
        # step_type_id = pk
        step_type_id = request.GET.get('step_type_id')
        print(step_type_id)
        form = StepForm(step_type_id=step_type_id)
        print(form)
        s_form = form.as_p()
        print(s_form)
        #TODO: Just return RENDERED FORM HTML (NOT SURE IF CASTING AS A STRING IS NEEDED)
        #return HttpResponse(form.as_p)
        #return JsonResponse({"form": form.as_p, "step_type_id": step_type_id})
        response = HttpResponse(str(s_form))
        # response['form'] = str(s_form)
        # response['step_type_id'] = step_type_id
        return response


def flow_form(request):

    if request.method == 'POST':

        project_id = request.POST.get('project_id')
        print(project_id)
        project = Project.objects.get(id=project_id)

        passed = request.POST.get("passed")
        if passed == 'false':
            passed = False
        elif passed == 'true':
            passed = True
        else:
            passed = None
        print(passed)
        name = request.POST.get("name")
        form = FlowForm(request.POST)

        if form.is_valid():
            Flow.objects.create(name=name, passed=passed, project=project)
            print("Cool")
            return HttpResponse(project.id)
        else:
            json_data = {"form": str(form.as_p()), "status": "Failed"}
            return JsonResponse(json_data)
    else:
        form = FlowForm()
        form = form.as_p()
        response = HttpResponse(str(form))
        return response


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