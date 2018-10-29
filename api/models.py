from django.db import models
import trippp.settings as conf
import os,sys

def delete_previous_file(function):

    def wrapper(*args, **kwargs):

        self = args[0]

        # 保存前のファイル名を取得
        result = Image.objects.filter(pk=self.pk)
        previous = result[0] if len(result) else None
        super(Image, self).save()

        # 関数実行
        result = function(*args, **kwargs)

        # 保存前のファイルがあったら削除
        if previous:
            os.remove(conf.MEDIA_ROOT + '/' + previous.image.name)
        return result
    return wrapper

# Create your models here.
class Image(models.Model):

    

    @delete_previous_file
    def delete(self, using=None, keep_parents=False):
        super(Image, self).delete()

    image = models.ImageField(upload_to='user_upload/')
    ref= models.BooleanField(default=1)
    owner=models.IntegerField()
    name=models.URLField()

    def __str__(self):
        return self.image.name
