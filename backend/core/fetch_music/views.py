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

class MediumPagination(PageNumberPagination):
    page_size_query_param = 'page_size'

class GetAPI(generics.ListCreateAPIView):
    pagination_class = MediumPagination
    serializer_class = SearchSerializer

    def get_queryset(self): #Paginated GET API
        queryset=Videos.objects.all().order_by('-published_at')
        return queryset
    
    def post(self,request): #for frontend call, without pagination
        queryset=Videos.objects.all().order_by('-published_at')
        res=queryset.values_list('video_id','title','description','published_at','thumbnail')
        return Response({"response":res})


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

class UpdateResultsOnce(generics.ListCreateAPIView):
    
    def post(self,request):
        url = 'https://www.googleapis.com/youtube/v3/search?part=snippet&key=AIzaSyAhiFH91JciYBdCT_U8A9hQ26bJyShVK3Q&type=video&q=official%20music&maxResults=100&order=date&publishedAfter=2021-05-23T00:00:00Z'
        r = requests.get(url, headers={'Content-Type':      
            'application/json'})
        response= r.json()
        for item in response['items']:
            video = Videos(video_id=item['id']['videoId'], title=item['snippet']['title'],description=item['snippet']['description'],
                            published_at=item['snippet']['publishedAt'],thumbnail=item['snippet']['thumbnails']['medium']['url'])
            video.save()
        return Response({"response":response})