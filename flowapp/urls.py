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
    path('get-step-form/', views.get_step_forms, name='get-form'),
    path('step-form/', views.step_form, name='step-form')
]

