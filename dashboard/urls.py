from django.urls import path, include
from users.forms import CustomUserUpdateForm
from . import views

urlpatterns = [
    path('', views.dashboard, name="dashboard"),
    path('exam/', views.ExamCreateView.as_view(), name="dashboard-exam"),
    path('siswa/<int:pk>/', views.ProfileDetailView.as_view(), name="detail-student"),
    path('ayah/<int:pk>/', views.FatherProfileDetailView.as_view(), name="detail-student-father"),
    path('ibu/<int:pk>/', views.MotherProfileDetailView.as_view(), name="detail-student-mother"),
    path('wali/<int:pk>/', views.GuardianProfileDetailView.as_view(), name="detail-student-guardian"),
    path('jurusan/<int:pk>/', views.MajorProfileDetailView.as_view(), name="detail-student-major"),
    path('berkas/<int:pk>/', views.FilesProfileDetailView.as_view(), name="detail-student-files"),
    path('score/<int:pk>/', views.ScoreListView.as_view(), name="detail-student-score"),
    path('score/<int:pk_user>/<int:pk>/delete/', views.ScoreDeleteView.as_view(), name="detail-student-score-delete"),
    path('score/<int:pk_user>/<int:pk>/passed/', views.ScorePassView.as_view(), name="detail-student-score-passed"),
    path('users/<int:pk>/', views.UpdateUser.as_view(), name="change-student-name"),
]
