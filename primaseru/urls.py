from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('profile/', views.studentProfile, name="profile"),
    path('profile/save/<str:data>/', views.save_profile, name="save-profile"),
]
