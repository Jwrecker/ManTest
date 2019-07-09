from django.contrib import admin

from .models import Flow, Step, StepType, Project


class FlowAdmin(admin.ModelAdmin):
    list_display = ('title', 'passed', 'project')
    search_fields = ['title', 'project']
    fields = ['title', 'project', 'passed']


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title',)
    fields = ('title',)


class StepAdmin(admin.ModelAdmin):
    list_display = ('flow', 'type', 'item')
    list_filter = ('flow', 'type', 'item')
    fields = ('flow', 'type', 'item', 'order', 'desired_result', 'passed', 'fixture_name')


class TypeAdmin(admin.ModelAdmin):
    list_display = ('step_type', 'has_fixture')
    fields = ('step_type', 'has_fixture')


admin.site.register(Flow, FlowAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Step, StepAdmin)
admin.site.register(StepType, TypeAdmin)
