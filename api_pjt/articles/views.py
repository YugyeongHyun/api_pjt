from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from .models import Article, Comment
from django.core import serializers
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializer import ArticleSerializer, CommentSeraializer, ArticleDetailSerializer
from rest_framework import status, viewsets
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .permissions import IsOwnerOrReadOnly


class ArticleListAPIView(APIView):
    def get(self, request):
        articles = Article.objects.all()
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data)

    def post(self, request):
        permission_classes = [IsAuthenticated]
        serializer = ArticleSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)


class ArticledetailAPIView(APIView):
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_object(self, pk):
        return get_object_or_404(Article, pk=pk)

    def get(self, request, pk):
        article = self.get_object(pk)
        serializer = ArticleDetailSerializer(article)
        return Response(serializer.data)

    def put(self, request, pk):
        article = self.get_object(pk)
        serializer = ArticleDetailSerializer(
            article, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

    def delete(self, request, pk):
        article = self.get_object(pk)
        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CommentListAPIView(APIView):
    def get(self, request, article_pk):
        article = get_object_or_404(Article, pk=article_pk)
        comments = article.comments.all()
        serializer = CommentSeraializer(comments, many=True)
        return Response(serializer.data)

    def post(self, request, article_pk):
        article = get_object_or_404(Article, pk=article_pk)
        serializer = CommentSeraializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(article=article)
            return Response(serializer.data, status=status.HTTP_201_CREATED)


class CommentDetailAPIView(APIView):
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def delete(self, request, comment_pk):
        comment = get_object_or_404(Comment, pk=comment_pk)
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self, request, comment_pk):
        comment = get_object_or_404(Comment, pk=comment_pk)
        serializer = CommentSeraializer(
            comment, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
