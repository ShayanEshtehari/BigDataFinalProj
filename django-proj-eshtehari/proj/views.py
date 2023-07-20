from django.shortcuts import render, redirect # new redirect

# Create your views here.
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

# from .models import Post

from .models import *  # new
from django.db.models import F, Avg, Count, Min, Sum  # new

# from django.contrib.auth.models import User # new

from rest_framework import viewsets # API
from .serializers import * # API
from rest_framework import permissions # API

from rest_framework.authtoken.views import ObtainAuthToken # API
from rest_framework.authtoken.models import Token # API
from rest_framework.response import Response # API

from rest_framework import generics, mixins # API

from datetime import datetime, timedelta
from rest_framework import viewsets
from rest_framework.response import Response
from django.db.models import Q

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import NewsModel

def home_view(request):
    return render(request, 'home.html', {})

def redir_view(request):
    return redirect('/api/')

# API
# class NewsViewSet(viewsets.ModelViewSet):
#     # queryset = NewsModel.objects.all().order_by('-id')
#     queryset = NewsModel.objects.all()
#     serializer_class = NewsSerializer


class NewsViewSet(viewsets.ModelViewSet):
    queryset = NewsModel.objects.all()
    serializer_class = NewsSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        author_name = self.request.query_params.get('author', None)
        category_name = self.request.query_params.get('category', None)

        if author_name:
            # queryset = queryset.filter(author__iexact=author_name)
            # queryset = queryset.filter(Q(author__iexact=author_name))
            queryset = [item for item in queryset if item.author.lower() == author_name.lower()]

        if category_name:
            queryset = [item for item in queryset if item.category.lower() == category_name.lower()]

        return queryset


class UniqueListView(viewsets.ModelViewSet):
    queryset = NewsModel.objects.all()
    serializer_class = NewsSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        author_name = self.request.query_params.get('author', None)
        category_name = self.request.query_params.get('category', None)

        if author_name:
            queryset = [item for item in queryset if item.author.lower() == author_name.lower()]

        if category_name:
            queryset = [item for item in queryset if item.category.lower() == category_name.lower()]

        return queryset

    # def get(self, request):
    #     authors = NewsModel.objects.values_list('author', flat=True).distinct()
    #     authors_list = list(authors)
    #     serializer = NewsSerializer({'author': authors_list}, many=True)
    #     return Response(serializer.data, status=status.HTTP_200_OK)
    
    def list(self, request, *args, **kwargs):
        # Retrieve all data from the NewsModel queryset
        queryset = self.get_queryset()

        # unique_authors = NewsModel.objects.values_list('author', flat=True).distinct()
        # unique_categories = NewsModel.objects.values_list('category', flat=True).distinct()
        unique_authors = set(item.author for item in queryset)
        unique_categories = set(item.category for item in queryset)

        # Prepare the response data
        response_data = {
            "unique_authors": list(unique_authors),
            "unique_categories": list(unique_categories)
        }

        return Response(response_data)
