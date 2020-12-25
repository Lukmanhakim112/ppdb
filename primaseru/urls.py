from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('profile/', views.studentProfile, name="profile"),
    path('profile/save/student/', views.save_student_profile, name="save-student"),
    path('profile/save/father/', views.save_father_profile, name="save-father"),
]
