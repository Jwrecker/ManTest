from django.db import models, transaction
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models import F, Max
import uuid

def truncated_uuid():
    return str(uuid.uuid4()).split("-")[0]


#TODO: REMOVE AFTER DEFINING
#FAKE_STEP_CHOICES = [
#    ('Load', 'Load URL'),
#    ('Click', 'Click On'),
#    ('Enter', 'Enter In'),
#    ('Set', 'Set'),
#    ('Verify', 'Verification'),
#]


DISALLOWED = 'D'
ALLOWED = 'A'
REQUIRED = 'R'

VALIDATION_CHOICES = [
    (DISALLOWED, 'Disallowed'),
    (ALLOWED, 'Allowed'),
    (REQUIRED, 'Required'),
]


class Error(Exception):
    pass


class NoOrderError(Error):
    pass


class PositionTooLowError(Error):
    pass


class NonConsecutiveError(Error):
    pass


class PositionTooHighError(Error):
    pass


class Project(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class FlowManager(models.Manager):
    def move(self, obj, new_order):
        # TODO COPY STUFF FROM STEP
        """ Move an object to a new order position """

        qs = self.get_queryset()
        if new_order is None:
            raise NoOrderError
        if new_order < 1:
            raise PositionTooLowError
        elif new_order > qs.filter(project=obj.project).count() + 1:
            raise PositionTooHighError
        else:
            with transaction.atomic():
                if obj.order > int(new_order):
                    qs.filter(
                        project=obj.project, order__lt=obj.order, order__gte=new_order
                    ).exclude(pk=obj.pk).update(order=F("order") + 1)
                else:
                    qs.filter(
                        project=obj.project, order__lte=new_order, order__gt=obj.order
                    ).exclude(pk=obj.pk).update(order=F("order") - 1)

                obj.order = new_order
                obj.save()

    def create(self, **kwargs):
        instance = self.model(**kwargs)

        with transaction.atomic():
            results = self.filter(
                project=instance.project
            ).aggregate(
                Max('order')
            )

            current_order = results['order__max'] + 1
            if current_order is None:
                current_order = 0

            value = current_order + 1
            instance.order = value
            instance.save()

            return instance


class Flow(models.Model):
    id = models.CharField(primary_key=True, default=truncated_uuid, editable=False, max_length=8)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    name = models.CharField(max_length=75)
    passed = models.BooleanField(default=False)
    order = models.IntegerField(default=1)

    objects = FlowManager()

    def __str__(self):
        return self.name


class StepManager(models.Manager):
    """ Manager to encapsulate bits of business logic """

    def move(self, obj, new_order, source_flow, target_flow):
        """ Move an object to a new order position (potentially in a new flow) """

        if new_order is None:
            raise NoOrderError
        if new_order < 1:
            raise PositionTooLowError
        qs = self.get_queryset()
        if new_order > qs.filter(flow=obj.flow).count() + 2:
            raise PositionTooHighError

        if source_flow == target_flow:
            # Moving position within a flow
            with transaction.atomic():
                # If you are moving the step to a lower position (closer to 1) ...
                if obj.order > int(new_order):
                    # ... take everything in between the old position and the new position and move them up one
                    qs.filter(
                        flow=obj.flow, order__lt=obj.order, order__gte=new_order
                    ).exclude(pk=obj.pk).update(order=F("order") + 1)
                # ... but if you're moving the step to higher position (or staying the same)
                else:
                    # ... lower the position of any step in between the old position and the new position
                    qs.filter(
                        flow=obj.flow, order__lte=new_order, order__gt=obj.order
                    ).exclude(pk=obj.pk).update(order=F("order") - 1)
                # ... and save the new position
                obj.order = new_order
                obj.save()
        else:
            # TODO Copy crap into here and fix
            # Moving position between flows
            with transaction.atomic():
                qs.filter(
                    flow=obj.flow, order__gte=obj.order
                ).exclude(pk=obj.pk).update(order=F("order") - 1)
            obj.flow = target_flow
            obj.order = new_order
            with transaction.atomic():
                qs.filter(
                    flow=obj.flow, order__gte=obj.order
                ).exclude(pk=obj.pk).update(order=F("order") + 1)
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
            current_order = results['order__max']
            if current_order is None:
                current_order = 0

            value = current_order + 1
            instance.order = value
            instance.save()

            return instance

    def insert(self, order, target_flow, **kwargs):
        s = Step.objects.create(flow=target_flow, **kwargs)
        Step.objects.move(s, order, target_flow, target_flow)

    def remove(self, obj):
        with transaction.atomic():
            Step.objects.all().filter(
                      flow=obj.flow, order__gte=obj.order
                 ).exclude(pk=obj.pk).update(order=F("order") - 1)
        Step.objects.get(pk=obj.pk, flow=obj.flow).delete()


class StepType(models.Model):
    name = models.CharField(unique=True, max_length=30)
    url_validation = models.CharField(
        max_length=1,
        choices=VALIDATION_CHOICES,
        default='ALLOWED'
    )
    has_verification = models.CharField(
        max_length=1,
        choices=VALIDATION_CHOICES,
        default='ALLOWED'
    )
    has_fixture = models.CharField(
        max_length=1,
        choices=VALIDATION_CHOICES,
        default='ALLOWED'
    )

    def __str__(self):
        if self.name:
            return str(self.name)
        else:
            return ""


class Step(models.Model):
    id = models.CharField(primary_key=True, default=truncated_uuid, editable=False, max_length=8)
    #id = models.UUIDField(primary_key=True, default=uuid.uuid4.split('-')[0], editable=False, )
    flow = models.ForeignKey(Flow, on_delete=models.CASCADE, null=False)
    order = models.IntegerField(default=1)
    step_type = models.ForeignKey(StepType, on_delete=models.PROTECT)
    desired_result = models.CharField(max_length=500, blank=True, null=True)
    passed = models.BooleanField(default=False, blank=True, null=True)
    fixture = models.CharField(max_length=100, blank=True, null=True)
    url = models.URLField(blank=True, null=True)

    objects = StepManager()

    def project(self):
        return self.flow.project
    project.short_description = 'Project'


    def __str__(self):
        truncated_id = str(self.id).split('-')[0]
        return f"Step {truncated_id} ({self.flow.project}-{self.flow.order}-{self.order})"
        #return str(self.flow.project) + str(self.flow) + " Step" + str(self.order)

    class Meta:
        index_together = ('flow', 'order')
        ordering = ['order']


    #def save(self, force_insert=False, force_update=False, using=None,
           #  update_fields=None):
        # Todo: do a bunch of checks based on self.StepType. (Or do in clean.)
        # Todo: Also I could just use custom validators on every form, including Admin
      #  pass



        #qs = self.get_queryset()

        #print(qs)

        #if obj.order > new_order:

        #    if new_order is None:
         #     raise TooSmallError
            #elif new_order > qs.count()+1:
             #   raise NotEnoughItemsError
           # else:

            #    obj.order = qs[new_order-1].order - .0000001

              #  obj.save()
        #else:
           # if new_order is None:
            #    raise NoOrderError
            #elif int(new_order) < 1:
            #    raise TooSmallError
            #elif new_order > qs.count() + 1:
            #    raise NotEnoughItemsError
            #else:

             #   obj.order = qs[new_order - 1].order + .0000001

              #  obj.save()
              #  obj.save()
