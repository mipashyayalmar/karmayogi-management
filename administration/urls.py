from django.urls import path
from . import views


urlpatterns = [
    

    path('designation', views.add_designation, name='designation'),
  
]
