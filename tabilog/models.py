from django.db import models
from tinymce import HTMLField
from datetime import datetime

class tabilog(models.Model):

    # Show in Web Page
    title=models.CharField(max_length=100)
    pub_date=models.DateTimeField(default=datetime.now)
    author=models.CharField(max_length=100)
    user_pk=models.IntegerField()
    body=HTMLField("content")

    # Use system processing
    script=models.TextField(verbose_name="content")
    is_editing=models.BooleanField(default=False)
    def __str__(self):
        return self.title

class Images(models.Model):
    src = models.ImageField('画像')
    target = models.ForeignKey(
        tabilog, verbose_name='Link to an article',
        blank=True, null=True,
        on_delete=models.SET_NULL
    )
