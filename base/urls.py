from django.urls import path
from .views import news_api, home, questions_api, mcq

urlpatterns = [
    path('', home, name='home'),
    path('news_api/', news_api, name='news_api'),
    path('questions/<str:news_uid>/', questions_api, name='questions_api'),
    path('mcq/<str:news_uid>/', mcq, name='mcq'),
]
