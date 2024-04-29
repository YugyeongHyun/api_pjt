from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import Article
from django.core import serializers
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializer import ArticleSerializer


@api_view(['GET'])
def article_list(request):
    articles = Article.objects.all()
    serializer = ArticleSerializer(articles, many=True)
    return Response(serializer.data)
