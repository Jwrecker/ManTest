# coding: utf-8
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ManTest.settings")
django.setup()

from flowapp.models import Project, Flow, Step, StepType

# Create step type (load)
load = StepType(title="Load", url_validation="Optional", has_verification="Optional", has_fixture="Optional")
load.save()

for i in range(1, 3): #Two of them
    p = Project(title=f"P{i}")
    p.save()
    for j in range(1, 3):
        f = Flow(project=p, title=f"P{i}_F{j}", order=j, passed="False")
        f.save()
        for k in range(1, 5):
            s = Step.objects.create(flow=f, type=load, order=k, item="URL")
            s.save()