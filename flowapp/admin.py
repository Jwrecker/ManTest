from django.contrib import admin

from .models import Flow, Action, ActionTypes, Project


class FlowAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'passed')
    search_fields = ['title']
    fields = ['title', 'passed']


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title',)
    fields = ('title',)


admin.site.register(Flow, FlowAdmin)
admin.site.register(Project, ProjectAdmin)