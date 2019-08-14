from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = "flowapp"
urlpatterns = [
    path('', views.ProjectListView.as_view(), name='main'),
    path('project/<int:pk>', views.ProjectDetailView.as_view(), name='project'),
    path('move-step/', views.move_step, name='move-step'),
    path('add-step/', views.add_step, name='add-step'),
    path('test-forms/', views.test_step_forms, name='test'),
    path('get-steps/', views.get_steps, name='get-steps'),
    path('get-flow/', views.get_flow, name='get_flow'),
    path('step-form/', views.step_form, name='step-form'),
    path('move-flow/', views.move_flow, name='move-flow'),
    path('get-flows/', views.get_flows, name='get-flows'),
    path('project-form/', views.project_form, name='project-form'),
    path('flow-form/', views.flow_form, name='flow-form'),
    path('delete-step/', views.delete_step, name='delete-step'),
    path('edit-step/', views.edit_step, name='edit-step'),
    path('delete-project/', views.delete_project, name='delete-project'),
    path('delete-flow/', views.delete_flow, name='delete-flow'),
    # path('step-form/<int:pk>', views.get_step_forms, name='step-form-get'
]

