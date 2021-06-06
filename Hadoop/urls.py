from django.urls import path
from . import views


urlpatterns = [
path('', views.Hadoop, name='hadoop'),
path('docs/', views.Docs, name='hadoopdocs'),  
path('upload/', views.upload, name="upload") 
]

