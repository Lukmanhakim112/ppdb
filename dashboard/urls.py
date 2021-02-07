from django.urls import path, include
from users.forms import CustomUserUpdateForm
from . import views

urlpatterns = [
    path('', views.dashboard, name="dashboard"),
    path('exam/', views.ExamCreateView.as_view(), name="dashboard-exam"),

    path('jadwal/pendaftaran/', views.RegisterSchedule.as_view(), name="schedule"),
    path('jadwal/pendaftaran/create/', views.RegisterScheduleCreateView.as_view(), name="schedule-create"),
    path('jadwal/pendaftaran/delete/<int:pk>/', views.RegisterSchduleDeleteView.as_view(), name="schedule-delete"),
    path('jadwal/pendaftaran/update/<int:pk>/', views.RegisterSchduleUpdateView.as_view(), name="schedule-update"),

    path('siswa/<int:pk>/', views.ProfileDetailView.as_view(), name="detail-student"),
    path('ayah/<int:pk>/', views.FatherProfileDetailView.as_view(), name="detail-student-father"),
    path('ibu/<int:pk>/', views.MotherProfileDetailView.as_view(), name="detail-student-mother"),
    path('wali/<int:pk>/', views.GuardianProfileDetailView.as_view(), name="detail-student-guardian"),
    path('jurusan/<int:pk>/', views.MajorProfileDetailView.as_view(), name="detail-student-major"),
    path('berkas/<int:pk>/', views.FilesProfileDetailView.as_view(), name="detail-student-files"),
    path('score/<int:pk>/', views.ScoreListView.as_view(), name="detail-student-score"),
    path('score/<int:pk_user>/<int:pk>/delete/', views.ScoreDeleteView.as_view(), name="detail-student-score-delete"),

    path('users/<int:pk>/', views.UpdateUser.as_view(), name="change-student-name"),
]
