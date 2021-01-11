from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.exam, name="exam"),
    path('list/', views.ExamView.as_view(), name="exam-list"),
    path('<int:pk>/question/add/', views.AddQuestion.as_view(), name="question-add"),
    path('<int:pk>/', views.ExamViewDetail.as_view(), name="exam-detail"),
    path('question/<int:pk>/', views.QuestionView.as_view(), name="question-list"),
    path('answer/<int:pk>/', views.AnswerView.as_view(), name="answer-list"),
]
