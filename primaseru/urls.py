from django.urls import path, include
from . import views, forms, models
from .views import ProfileView

urlpatterns = [
    path('', views.home, name="home"),
    path('profile/', views.studentProfile, name="profile"),
    # path('profile/berkas/', views.studentFiles, name="berkas"),
    path('profile/ayah/', ProfileView.as_view(), name="profile-ayah"),
    path('profile/ibu/', ProfileView.as_view(form_class=forms.MotherStudentProfileForm, models=models.MotherStudentProfile, name="ibu"), name="profile-ibu"),
    path('profile/siswa/', ProfileView.as_view(form_class=forms.StudentProfileForm, models=models.StudentProfile, name="siswa"), name="profile-siswa"),
    path('profile/wali/', ProfileView.as_view(form_class=forms.StudentGuardianProfileForm, models=models.StudentGuardianProfile, name="wali"), name="profile-wali"),
    path('profile/jurusan/', ProfileView.as_view(form_class=forms.MajorStudentForm, models=models.MajorStudent, template_name="primaseru/major.html",
                                                 name="jurusan"), name="jurusan-siswa"),
    path('profile/berkas/', ProfileView.as_view(form_class=forms.StudentFileForm, models=models.StudentFile, template_name="primaseru/student_files.html",
                                                name="berkas"), name="berkas-siswa"),
]
