from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Project(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title


class Flow(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    title = models.CharField(max_length=75)
    passed = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class ActionTypes(models.Model):
    type = models.CharField(max_length=100)

    def __str__(self):
        return self.type


class Action(models.Model):
    flow = models.ForeignKey(Flow, on_delete=models.CASCADE)
    # TODO either foreignkey to Types or Choices Field
    type = models.ForeignKey(ActionTypes, on_delete=models.CASCADE)
    more = models.CharField(max_length=200, blank=True, null=True)
    desired_result = models.CharField(max_length=500)
    passed = models.BooleanField(default=False)

    def __str__(self):
        return self.type + ": " + self.more

