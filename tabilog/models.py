from django.db import models
from tinymce import HTMLField
from datetime import datetime
import os,sys
import trippp.settings as settings

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

def delete_previous_file(function):
    """不要となる古いファイルを削除する為のデコレータ実装.

    :param function: メイン関数
    :return: wrapper
    """
    def wrapper(*args, **kwargs):
        """Wrapper 関数.

        :param args: 任意の引数
        :param kwargs: 任意のキーワード引数
        :return: メイン関数実行結果
        """
        self = args[0]

        # 保存前のファイル名を取得
        result = Images.objects.filter(pk=self.pk)
        previous = result[0] if len(result) else None
        super(Images, self).save()

        # 関数実行
        result=function(*args, **kwargs)

        # 保存前のファイルがあったら削除
        if previous:
            os.remove(settings.MEDIA_ROOT + '/' + previous.src.name)
        return result
    return wrapper

class Images(models.Model):

    @delete_previous_file
    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        super(Images, self).save()

    @delete_previous_file
    def delete(self, using=None, keep_parents=False):
        super(Images, self).delete()

    src = models.ImageField(
        '画像',upload_to="user_upload/",
        )
    target = models.ForeignKey(
        tabilog, verbose_name='Link to an article',
        blank=True, null=True,
        on_delete=models.SET_NULL
    )
