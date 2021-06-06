from django.urls import path
from . import views


urlpatterns = [
    path('', views.Docker, name='docker'),
    path('docs/', views.Docs, name='dockerdocs'),
    path('service/', views.Docker_service, name='docker_service'),
    path('terminate/', views.Terminate_model, name='terminate_model'),
]

