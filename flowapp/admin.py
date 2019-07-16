from django.contrib import admin

from .models import Flow, Step, StepType, Project


class ProjectFilter(admin.SimpleListFilter):
    title= 'project'
    parameter_name = 'project'

    def lookups(self, request, model_admin):
        return self.all()

    def queryset(self, request, queryset):
        return queryset.filter(project=self.value())

class FlowAdmin(admin.ModelAdmin):
    list_display = ('order', 'title', 'passed', 'project')
    search_fields = ['title', 'project']
    fields = ['title', 'project', 'order', 'passed']


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title',)
    fields = ('title',)


class StepAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'project', 'flow', 'order', 'type', 'item')
    list_filter = (ProjectFilter, 'flow')
    fields = ('flow', 'type', 'item', 'order', 'desired_result', 'passed', 'fixture_name')


class TypeAdmin(admin.ModelAdmin):
    list_display = ('title',)
    fields = ('title', 'url_validation', 'has_fixture', 'has_verification')


admin.site.register(Flow, FlowAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Step, StepAdmin)
admin.site.register(StepType, TypeAdmin)
