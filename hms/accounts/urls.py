
from django.urls import path
from . import views

urlpatterns = [

    path('register/', views.register, name='register'),
    path('testing/', views.testing, name='testing'),
    path('student/', views.student_details_view, name='student')
]
