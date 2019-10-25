from . import views
from django.urls import path

urlpatterns = [
    path('addpost/', views.post_new, name='addpost'),
    path('notices', views.PostList.as_view(), name='notices'),
    path('noticesstud', views.PostListStud.as_view(), name='noticesstud'),
    path('delete/<str:tag>', views.post_delete, name='delete'),
]