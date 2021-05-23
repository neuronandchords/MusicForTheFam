import os
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import generics
from youtube_search import YoutubeSearch
from googleapiclient.discovery import build
import requests
from .models import Videos
from django.views.decorators.csrf import csrf_exempt
from asgiref.sync import sync_to_async
from celery.decorators import task
from celery.task.schedules import crontab
from celery.decorators import periodic_task
from datetime import timedelta


@periodic_task(
    run_every=timedelta(seconds=30),
    name="get_youtube_videos",
    ignore_result=True
)
def get_youtube_videos():
    url = 'https://www.googleapis.com/youtube/v3/search?part=snippet&key=AIzaSyAhiFH91JciYBdCT_U8A9hQ26bJyShVK3Q&type=video&q=official%20music&maxResults=100&order=date'
    r = requests.get(url, headers={'Content-Type':      
        'application/json'})
    response= r.json()
    for item in response['items']:
        video = Videos(video_id=item['id']['videoId'], title=item['snippet']['title'],description=item['snippet']['description'],
                        published_at=item['snippet']['publishedAt'],thumbnail=item['snippet']['thumbnails']['medium']['url'])
        video.save()
    print("done!")
    return response