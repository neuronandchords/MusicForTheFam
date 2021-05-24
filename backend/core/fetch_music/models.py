from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.text import slugify

class Videos(models.Model):
    # Two character identifer for country (us, pk, in, etc.)
    video_id = models.CharField(max_length=50,primary_key=True)
    title = models.CharField(max_length=500)
    description = models.CharField(max_length=500,default="Official Music")
    published_at = models.DateTimeField()
    thumbnail= models.URLField(default='https://upload.wikimedia.org/wikipedia/commons/3/35/Simple_Music.svg')

    class Meta:
        db_table = "videos"

    def __str__(self):
        return f"{self.video_id} ({self.title})"