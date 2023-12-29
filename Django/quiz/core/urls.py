from django.urls import path, re_path
from rest_framework import permissions

from .views import *

app_name = "core"

urlpatterns = [
    path('course/create/', CourseCreateView.as_view()),
    path('course/<int:course_id>/', CourseRetrieveView.as_view()),
    path('quiz/create/', QuizCreateView.as_view()),
    path('quiz/<int:quiz_id>/', QuizRetrieveView.as_view()),
]