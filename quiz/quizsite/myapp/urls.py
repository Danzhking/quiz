from django.urls import path
from . import views

urlpatterns = [
    path('quiz/', views.quiz_view, name='quiz-view'),
    path('', views.index, name='index'),
    path('result/', views.result_page, name='result-page'),
]
