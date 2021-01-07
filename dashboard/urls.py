from django.urls import path, include
from primaseru import models as prim_models
from . import views, forms

urlpatterns = [
    path('', views.dashboard, name="dashboard"),
    path('siswa/<int:pk>/', views.ProfileDetailView.as_view(), name="detail-student"),
    path('ayah/<int:pk>/', views.ProfileDetailView.as_view(form_class=forms.DashboardFatherForm, model=prim_models.FatherStudentProfile), name="detail-student-father"),
    path('ibu/<int:pk>/', views.ProfileDetailView.as_view(form_class=forms.DashboardMotherForm, model=prim_models.MotherStudentProfile), name="detail-student-mother"),
    path('wali/<int:pk>/', views.ProfileDetailView.as_view(form_class=forms.DashboardGuardianForm, model=prim_models.StudentGuardianProfile), name="detail-student-guardian"),
    path('jurusan/<int:pk>/', views.ProfileDetailView.as_view(form_class=forms.DashboardMajorForm, model=prim_models.MajorStudent), name="detail-student-major"),
    path('berkas/<int:pk>/', views.ProfileDetailView.as_view(form_class=forms.DashboardFilesForm, model=prim_models.StudentFile), name="detail-student-files"),
]
