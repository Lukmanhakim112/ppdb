from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('profile/', views.studentProfile, name="profile"),
    path('profile/ayah/', views.ProfileView.as_view(), name="profile-ayah"),
    path('profile/ibu/', views.MoatherProfileView.as_view(), name="profile-ibu"),
    path('profile/siswa/', views.StudentProfileView.as_view(), name="profile-siswa"),
    path('profile/wali/', views.GuardianProfileView.as_view(), name="profile-wali"),
    path('profile/jurusan/', views.MajorStudentView.as_view(), name="jurusan-siswa"),
    path('profile/berkas/', views.FilesStudentView.as_view(), name="berkas-siswa"),
]
