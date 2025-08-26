from django.urls import path
from .views import execute_metta


urlpatterns = [
    path('execute/', execute_metta, name='execute_metta'),
]

