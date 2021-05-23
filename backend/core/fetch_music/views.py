import os
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import generics
from youtube_search import YoutubeSearch
from googleapiclient.discovery import build
import requests
from .models import Videos
from .serializers import SearchSerializer
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q, ExpressionWrapper, BooleanField, Count

class QueryYoutube(generics.ListCreateAPIView):

    def post(self,request):
        return Response({"message":"hello"})

class MediumPagination(PageNumberPagination):
    page_size_query_param = 'page_size'

class GetAPI(generics.ListCreateAPIView):
    pagination_class = MediumPagination
    serializer_class = SearchSerializer

    def get_queryset(self):
        queryset=Videos.objects.all().order_by('-published_at')
        return queryset

class SearchAPI(generics.ListCreateAPIView):
    pagination_class = MediumPagination
    serializer_class = SearchSerializer

    def post(self,request):
        search=request.data.get('search')
        if search:
            # expression = Q(title__icontains=search+" ") | Q(description__icontains=" "+search)
            queryset=Videos.objects.all().filter(Q(title__icontains=search) | Q(description__icontains=search))
            # is_match = ExpressionWrapper(expression, output_field=BooleanField())
            # queryset = queryset.annotate(my_field=is_match)
            # queryset = queryset.order_by('-publisd')
            res=queryset.values_list('video_id','title','description','published_at','thumbnail')
            return Response({"response":res})
        else:
            return Response({"enter a search query!"})
