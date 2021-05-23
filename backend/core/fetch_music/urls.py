from django.urls import path

from . import views

urlpatterns = [
    path('get_all_videos',views.GetAPI.as_view(), name='get all videos stored in DB'),
    path('search',views.SearchAPI.as_view(), name='search for videos in DB'),
    path('update',views.UpdateResultsOnce.as_view(), name= 'update results one time')
]