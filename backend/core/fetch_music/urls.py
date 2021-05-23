from django.urls import path

from . import views

urlpatterns = [
    path('sayhello', views.QueryYoutube.as_view(), name='hit youtube every 20seconds for results'),
    path('get_all_videos',views.GetAPI.as_view(), name='get all videos stored in DB'),
    path('search',views.SearchAPI.as_view(), name='search for videos in DB')
]