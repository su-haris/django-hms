
from django.urls import path
from . import views

urlpatterns = [

    path('register/', views.register, name='register'),
    path('testing/', views.testing, name='testing'),
    path('student/', views.student_details_view, name='student'),
    path('rooms/', views.room_all_view, name='rooms'),
    # path('roomselect/', views.room_select, name='roomselect')
    path('roomselect/<str:tag>', views.room_select, name='roomselect'),
    path('addroom/', views.addroom, name='addroom'),

]
