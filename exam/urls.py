from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.ExamView.as_view(), name="exam-list"),
    path('<int:pk>/', views.ExamViewDetail.as_view(), name="exam-detail"),
    path('<int:pk>/question/add/', views.AddQuestion.as_view(), name="question-add"),
    path('<int:pk_exam>/question/<int:pk>/delete/', views.QuestionDeleteView.as_view(), name="question-delete"),
    path('question/<int:pk>/', views.QuestionView.as_view(), name="question-list"),
    path('answer/<int:pk>/', views.AnswerView.as_view(), name="answer-list"),
]
