from django.db import models, transaction
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models import F, Max

#TODO: REMOVE
FAKE_STEP_CHOICES = [
    ('Load', 'Load URL'),
    ('Click', 'Click On'),
    ('Enter', 'Enter In'),
    ('Set', 'Set'),
    ('Verify', 'Verification'),
]

VALIDATION_CHOICES = [
    ('Disallowed', 'Disallowed'),
    ('Optional', 'Optional'),
    ('Required', 'Required'),
]


class Error(Exception):
    pass


class NoOrderError(Error):
    pass


class TooSmallError(Error):
    pass


class NonConsecutiveError(Error):
    pass


class NotEnoughItemsError(Error):
    pass


class Project(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title


class FlowManager(models.Manager):

    def move(self, obj, new_order):
        qs = self.get_queryset()
        results = self.filter(
            flow=obj.flow
        ).aggregate(
            Max('order')
        )
        current_order = results['order__max'] + 1

        while True:

            if new_order is None:
                raise NoOrderError
            elif int(new_order) < 1:
                raise TooSmallError
            elif int(new_order) > int(current_order):
                raise NonConsecutiveError

            with transaction.atomic():
                if obj.order > int(new_order):
                    qs.filter(
                        project=obj.flow,
                        order__lt=obj.order,
                        order__gte=new_order,
                    ).exclude(
                        pk=obj.pk
                    ).update(
                        order=F('order') + 1
                    )
                else:
                    qs.filter(
                        flow=obj.flow,
                        order__lte=new_order,
                        order__gt=obj.order,
                    ).exclude(
                        pk=obj.pk
                    ).update(
                        order=F('order') - 1,
                    )
                obj.order = new_order
                obj.save()
                break

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
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    title = models.CharField(max_length=75)
    passed = models.BooleanField(default=False)
    order = models.IntegerField(default=1)

    objects = FlowManager()

    def __str__(self):
        return self.title


class StepType(models.Model):
    title = models.CharField(max_length=15, null=True)
    url_validation = models.CharField(
        max_length=15,
        choices=VALIDATION_CHOICES,
        default='Optional'
    )
    has_verification = models.CharField(
        max_length=15,
        choices=VALIDATION_CHOICES,
        default='Optional'
    )
    has_fixture = models.CharField(
        max_length=15,
        choices=VALIDATION_CHOICES,
        default='Optional'
    )

    def __str__(self):
        if self.title:
            return str(self.title)
        else:
            return ""


class StepManager(models.Manager):
    """ Manager to encapsulate bits of business logic """

    def move(self, obj, new_order):
        """ Move an object to a new order position """

        qs = self.get_queryset()
        if new_order is None:
            raise NoOrderError
        if new_order < 1:
            raise TooSmallError
        elif new_order > qs.filter(flow=obj.flow).count()+1:
            raise NotEnoughItemsError
        else:
            with transaction.atomic():
                if obj.order > int(new_order):
                    qs.filter(
                        flow=obj.flow, order__lt=obj.order, order__gte=new_order
                    ).exclude(pk=obj.pk).update(order=F("order") + 1)
                else:
                    qs.filter(
                        flow=obj.flow, order__lte=new_order, order__gt=obj.order
                    ).exclude(pk=obj.pk).update(order=F("order") - 1)

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
            current_order = results['order__max']
            if current_order is None:
                current_order = 0

            value = current_order + 1
            instance.order = value
            instance.save()

            return instance


class Step(models.Model):

    flow = models.ForeignKey(Flow, on_delete=models.CASCADE)
    order = models.IntegerField(default=1)
    type = models.ForeignKey(StepType, on_delete=models.PROTECT)
    desired_result = models.CharField(max_length=500, blank=True, null=True)
    passed = models.BooleanField(default=False, blank=True, null=True)
    has_fixture = models.BooleanField(default=False)
    fixture_name = models.CharField(max_length=100, blank=True, null=True)
    if type == 'Load':
        item = models.URLField(blank=True, null=True)
    else:
        item = models.CharField(max_length=100, blank=True, null=True)

    objects = StepManager()

    def __str__(self):
        if self.item:
            return str(self.order) + " " + str(self.type) + ": " + self.item
        else:
            return str(self.order) + ": " + str(self.type)

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
