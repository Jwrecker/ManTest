from django.contrib import admin
from .models import StepType, Project, Flow, Step


class TypeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    fields = ('name', 'url_validation', 'has_fixture', 'has_verification')


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('name',)
    fields = ('name',)


class FlowAdmin(admin.ModelAdmin):
    list_display = ('name', 'project', 'order', 'passed')
    search_fields = ['name', 'project']
    ordering = ('project', 'order',)
    fields = ['name', 'project', 'order', 'passed']


class StepAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'project', 'flow', 'order', 'step_type', 'item')
    list_filter = ('flow__project', 'flow')
    ordering = ('flow__project', 'flow', 'order')
    fields = ('flow', 'step_type', 'item', 'order', 'desired_result', 'passed', 'fixture_name')


admin.site.register(StepType, TypeAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Flow, FlowAdmin)
admin.site.register(Step, StepAdmin)