from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = "flowapp"
urlpatterns = [
    path('', views.IndexView.as_view(), name='main'),
    path('project/<int:pk>', views.ProjectView.as_view(), name='project'),
    path('move-step/', views.move_step, name='move-step'),
]
