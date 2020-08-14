from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    # path('accounts/sign_up/', views.sign_up, name="sign_up"),
    path('profile_photo/', views.profile_photo, name='profile_photo'),
    path('all_users/', views.all_users, name='all_users'),
    path('create/<str:second_user_id>/', views.create_chat, name='create_chat'),
    path('<str:room_name>/', views.room, name='room'),
]