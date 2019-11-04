
from django.urls import path, include
from . import views

urlpatterns = [

    path('register/', views.register, name='register'),
    path('testing/', views.testing, name='testing'),
    path('student/', views.student_details_view, name='student'),
    path('rooms/', views.room_all_view, name='rooms'),
    # path('roomselect/', views.room_select, name='roomselect')
    # path('roomselect/<str:tag>', views.room_select, name='roomselect'),
    path('roomselect/<str:tag>', views.room_select_new, name='roomselect'),
    path('roomstud/<str:tag>', views.room_details, name='roomdetails'),
    path('warden', views.room_all_view_warden, name='wardenhome'),
    path('addroom/', views.addroom, name='addroom'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('update/', views.update, name='update'),
    path('changeroom/', views.room_change_view, name='changeroom'),
    path('roomchangeap/<str:tag>', views.room_change, name='roomchangeap'),
    path('applist/', views.approve_all_view_warden, name='applist'),
    path('applistnew/', views.new_approve_all_view_warden, name='applistnew'),
    path('appconfirm/<str:tag>', views.approve_confirm, name='appconfirm'),
    path('roomcheck', views.room_change_check, name='roomcheck'),
    path('reject/<str:tag>', views.approve_reject, name='reject'),
    path('history', views.fee_student_history, name='history'),
    path('topay', views.fee_instructions, name='topay'),
    path('feeregister/<str:tag>', views.fee_register, name='feeregister'),
    path('feesall', views.fee_approval_list, name='feesall'),
    path('feeconfirm/<str:tag>', views.fees_approve_confirm, name='feeconfirm'),
    path('feereject/<str:tag>', views.fees_approve_reject, name='feereject'),
    path('studsall', views.all_student, name='studsall'),
    path('studetail/<str:tag>', views.student_profile_admin, name='studetail'),
    path('rejectnew/<str:tag>', views.reject_form, name='rejectnew'),
    path('appconfirmnew/<str:tag>', views.approve_confirm_new, name='appconfirmnew'),
    path('rejectfee/<str:tag>', views.reject_form, name='rejectfee'),
    path('feestatus', views.fee_status, name='feestatus'),

]
