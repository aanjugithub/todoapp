from django.urls import path
from api import views

urlpatterns=[
    path('register/',views.RegistrationView.as_view())
    
] 

