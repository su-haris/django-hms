
from django.urls import path, include
from . import views

urlpatterns = [

    path('register/', views.register, name='register'),
    path('testing/', views.testing, name='testing'),
    path('student/', views.student_details_view, name='student'),
    path('rooms/', views.room_all_view, name='rooms'),
    # path('roomselect/', views.room_select, name='roomselect')
    path('roomselect/<str:tag>', views.room_select, name='roomselect'),
    path('roomstud/<str:tag>', views.room_details, name='roomdetails'),
    path('warden', views.room_all_view_warden, name='wardenhome'),
    path('addroom/', views.addroom, name='addroom'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('update/', views.update, name='update'),
    path('changeroom/', views.room_change_view, name='changeroom'),
    path('roomchangeap/<str:tag>', views.room_change, name='roomchangeap'),
    path('applist/', views.approve_all_view_warden, name='applist'),
    path('appconfirm/<str:tag>', views.approve_confirm, name='appconfirm'),
    path('roomcheck', views.room_change_check, name='roomcheck'),
    path('reject/<str:tag>', views.approve_reject, name='reject'),
    path('history', views.fee_student_history, name='history'),

]
