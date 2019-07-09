from django.db import models, transaction
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models import F, Max


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


class StepType(models.Model):
    STEP_CHOICES = [
        ('Load', 'Load URL'),
        ('Click', 'Click On'),
        ('Enter', 'Enter In'),
        ('Set', 'Set'),
        ('Verify', 'Verification'),
    ]
    step_type = models.CharField(
        max_length=15,
        choices=STEP_CHOICES,
    )
    has_fixture = models.BooleanField()

    def __str__(self):
        return self.step_type


class Step(models.Model):

    flow = models.ForeignKey(Flow, on_delete=models.CASCADE)
    order = models.IntegerField()
    type = models.ForeignKey(StepType, on_delete=models.PROTECT)
    desired_result = models.CharField(max_length=500, blank=True, null=True)
    passed = models.BooleanField(default=False, blank=True, null=True)
    fixture_name = models.CharField(max_length=100, blank=True, null=True)
    if type == 'Load':
        item = models.URLField(blank=True, null=True)
    else:
        item = models.CharField(max_length=100, blank=True, null=True)

    objects = StepManager()

    def __str__(self):
        return str(self.type) + ": " + self.item

    #def save(self, force_insert=False, force_update=False, using=None,
           #  update_fields=None):
        # Todo: do a bunch of checks based on self.StepType. (Or do in clean.)
        # Todo: Also I could just use custom validators on every form, including Admin
      #  pass


class StepManager(models.Manager):

    def move(self, obj, new_order):
        # Move an object to a new order position
        qs = self.get_queryset()

        with transaction.atomic():
            if obj.order > int(new_order):
                qs.filter(
                    flow=obj.flow,
                    order__lt=obj.order,
                    order__gte=new_order,
                ).exclude(pk=obj.pk).update(order=F('order') + 1,)

            else:
                qs.filter(
                    flow=obj.flow,
                    order__lte=new_order,
                    order__gt=obj.order,
                ).exclude(
                    pk=obj.pk,
                ).update(
                    order=F('order') - 1,
                )

                obj.order = new_order
                obj.save()

    def create(self, **kwargs):
        instance = self.model(**kwargs)

        with transaction.atomic():
            # Get our current max order number
            results = self.filter(
                flow=instance.flow
            ).aggregate(
                Max('order')
            )

            # Increment and use it for our new object
            current_order = results['order__max'] + 1
            if current_order is None:
                current_order = 0

            value = current_order + 1
            instance.order = value
            instance.save()

            return instance

    class Meta:
        index_together = ('flow', 'order')
