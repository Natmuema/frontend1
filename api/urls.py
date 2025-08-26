from django.urls import path
from .views import execute_metta, register, login, logout


urlpatterns = [
    path('execute/', execute_metta, name='execute_metta'),
    path('register', register, name='register'),
    path('login', login, name='login'),
    path('logout', logout, name='logout'),
]

