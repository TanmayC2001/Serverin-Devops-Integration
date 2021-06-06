from django.urls import path
from . import views

urlpatterns = [
    path('', views.AWS, name='aws'),
    path('docs/', views.Docs, name='awsdocs'),
    path('services/', views.Services, name='service'),
    path('instances/', views.Instances, name='instances'),
    path('terminate/', views.Terminate_instance, name='terminate_instance'),
    path('wordpress/', views.Wordpress, name="wordpress"),
    path('web_dev/', views.Web_dev, name="web_dev"),
    
]
