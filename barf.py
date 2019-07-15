# coding: utf-8
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ManTest.settings")
django.setup()

from flowapp.models import Project, Flow, Step, StepType

# Create step type (load)
load = StepType(title="Load", url_validation="Optional", has_verification="Optional", has_fixture="Optional")
load.save()

# Create Project
p = Project(title="Project")
p.save()

# Create Flow
f1 = Flow(project=p, title="Flow1", order=1, passed="False")
f1.save()

# Create Flow #2
f2 = Flow(project=p, title="Flow2", order="2", passed="False")

# Create Flow #3
f3 = Flow(project=p, title="Flow3", order="3", passed="False")

# Create Steps, s_(Flow#)_(Step#)
s_1_1 = Step(flow=f1, type=load, item="URL")
s_1_1.save()
s_1_2 = Step.objects.create(flow=f1, type=load, item="Login")
s_1_2.save()
s_1_3 = Step.objects.create(flow=f1, type=load, item="Logout")
s_1_3.save()

# Print step list
print(f1)
print(s_1_1)
print(s_1_2)
print(s_1_3)

# Change step 1 order to 3
Step.objects.move(s_1_1, 3)

print(f1)
print(s_1_1)
print(s_1_2)
print(s_1_3)
