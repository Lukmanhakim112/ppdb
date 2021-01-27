from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.ExamView.as_view(), name="exam-list"),
    # Exam Path
    path('<int:pk>/', views.ExamViewDetail.as_view(), name="exam-detail"),
    path('<int:pk>/update/', views.ExamUpdateView.as_view(), name="exam-update"),
    path('<int:pk>/delete/', views.ExamDeleteView.as_view(), name="exam-delete"),
    path('<int:pk>/enroll/', views.ExamEnrollView.as_view(), name="exam-enroll"),
    path('<int:pk>/timer/', views.ExamTimerView.as_view(), name="exam-timer"),
    # Question Path
    path('<int:pk>/question/add/', views.AddQuestion.as_view(), name="question-add"),
    path('<int:pk_exam>/taken/', views.TakeExamView.as_view(), name="taken-question"),
    path('<int:pk_exam>/taken/submit/', views.SubmitAnswer.as_view(), name="submit-question"),
    path('<int:pk_exam>/taken/<int:pk>/', views.RetriveAnswer.as_view(), name="question-answer"),
    path('<int:pk_exam>/question/<int:pk>/delete/', views.QuestionDeleteView.as_view(), name="question-delete"),
    path('<int:pk_exam>/question/<int:pk>/update/', views.QuestionUpdateView.as_view(), name="question-update"),
    path('answer/<int:pk>/', views.AnswerView.as_view(), name="answer-list"),
]
