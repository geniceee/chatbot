from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<str:room_name>/', views.room, name='room'),
    path('profile_photo/', views.profile_photo, name='profile_photo'),
    # path('success', views.success, name = 'success')
]

