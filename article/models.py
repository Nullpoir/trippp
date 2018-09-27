from django.db import models
from tinymce import HTMLField
from datetime import datetime

# Create your models here.

class doc(models.Model):
    title=models.CharField(max_length=100)
    pub_date=models.DateTimeField(default=datetime.now)
    body=HTMLField("content")
    def __str__(self):
        return self.title
