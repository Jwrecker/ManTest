# coding: utf-8
import os
import django
import argparse

# Setup the Django environment and do Django imports
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ManTest.settings")
django.setup()

from flowapp.models import StepType, Project, Flow, Step
from django.db.utils import IntegrityError
from django.db.models.base import ObjectDoesNotExist

# Setup argparse
parser = argparse.ArgumentParser(description='Reset elements of the ManTest DB')
parser.add_argument('--killprojects',
                    default=False,
                    action='store_true',
                    help='Kill Projects (and downstream items)!')
parser.add_argument('--killsteptypes',
                    default=False,
                    action='store_true',
                    help='Kill StepTypes!')
parser.add_argument('--killall',
                    default=False,
                    action='store_true',
                    help='Kill all the things, including Projects and StepTypes!')
parser.add_argument('--skipcreate', default=False, action='store_true', help="Don't create all the things!")
args = parser.parse_args()


def delete_projects():
    print("You gonna die, projects!")
    projects = Project.objects.all()
    for p in projects:
        p.delete()
    #Project.objects.all().delete()


def delete_step_types():
    print("You gonna die, step types!")
    step_types = StepType.objects.all()
    for st in step_types:
        st.delete()
    #StepType.objects.all().delete()


def create_objects():
    print("Making them goodies!")
    FAKE_STEP_TYPE_NAME = 'Fake'
    TEST_PROJECT_NAME = 'TP'

    # Create a fake step type, if none already exists
    try:
        fake_type = StepType.objects.get(name=FAKE_STEP_TYPE_NAME)
    except ObjectDoesNotExist:
        # DoesNotExist
        fake_type = StepType(name=FAKE_STEP_TYPE_NAME)
        fake_type.save()

    # Create a test project, if none already exists
    try:
        tp = Project.objects.get(name=TEST_PROJECT_NAME)
    except ObjectDoesNotExist:
        tp = Project(name=TEST_PROJECT_NAME)
        tp.save()

    # Create 2 test flows ...
    for j in range(1, 3):
        #TODO
        f = Flow(project=tp, name=f"{tp}_F{j}", order=j, passed="False")
        f.save()
        # Create 4 steps of our fake type to each
        for k in range(1, 5):
            s = Step.objects.create(flow=f, step_type=fake_type, order=k, item="URL")
            s.save()


if args.killall or args.killprojects:
    delete_projects()

if args.killall or args.killsteptypes:
    pass
    #TODO call the below after we have a good fixture solution in place
    #delete_step_types()

if not args.skipcreate:
    create_objects()
