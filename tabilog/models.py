from django.db import models
from tinymce import HTMLField
from datetime import datetime


class tabilog(models.Model):
    title=models.CharField(max_length=100)
    pub_date=models.DateTimeField(default=datetime.now)
    author=models.CharField(max_length=100)
    user_pk=models.IntegerField()
    thumbnail = models.ImageField(upload_to='thambnail/')
    body=HTMLField("content")
    content=HTMLField("content")
    def __str__(self):
        return self.title
