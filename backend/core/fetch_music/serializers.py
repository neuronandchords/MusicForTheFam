from rest_framework import serializers
from .models import Videos

class SearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Videos
        fields = ['video_id','title','description','published_at','thumbnail']