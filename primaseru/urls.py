from django.urls import path, include
from . import views, forms, models
from .views import ParentView

urlpatterns = [
    path('', views.home, name="home"),
    path('profile/', views.studentProfile, name="profile"),
    path('profile/ayah/', ParentView.as_view(), name="profile-ayah"),
    path('profile/ibu/', ParentView.as_view(form_class=forms.MotherStudentProfileForm, models=models.MotherStudentProfile, name="ibu"), name="profile-ibu"),
    path('profile/wali/', ParentView.as_view(form_class=forms.StudentGuardianProfileForm, models=models.StudentGuardianProfile, name="wali"), name="profile-wali"),
    path('profile/save/<str:data>/', views.save_profile, name="save-profile"),
]
