from django.shortcuts import render
from .models import News, Question
from django.http import JsonResponse
from django.utils import translation
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import QuestionSerializer, NewsSerializer

# Create your views here.
def home(request):
    lang = request.GET.get('lang', 'en')
    translation.activate(lang)
    return render(request, 'home.html')

def mcq(request, news_uid):
    lang = request.GET.get('lang', 'en')
    translation.activate(lang)
    return render(request, 'mcq.html', {'news_uid': news_uid})

@api_view(['GET'])
def questions_api(request, news_uid):
    lang = request.GET.get('lang', 'en')
    translation.activate(lang)
    
    questions = Question.objects.filter(news__uid=news_uid)
    serializer = QuestionSerializer(questions, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def news_api(request):
    from rest_framework.pagination import PageNumberPagination
    
    news = News.objects.filter(questions_generated=True).order_by('-created_at')
    
    # Apply pagination
    paginator = PageNumberPagination()
    paginator.page_size = 12
    paginated_news = paginator.paginate_queryset(news, request)
    
    serializer = NewsSerializer(paginated_news, many=True)
    return paginator.get_paginated_response(serializer.data)
