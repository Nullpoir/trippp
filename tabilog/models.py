from django.db import models
from tinymce import HTMLField
from datetime import datetime


class tabilog(models.Model):
    title=models.CharField(max_length=40)
    pub_date=models.DateTimeField(default=datetime.now)
    author=models.CharField(max_length=30)
    user_pk=models.IntegerField()
    tag=models.CharField(max_length=100)
    thumbnail = models.ImageField(upload_to='thambnail/',blank=True)
    body=HTMLField("body")
    content=HTMLField("content")
    index=HTMLField("index",blank=True)
    def __str__(self):
        return self.title
