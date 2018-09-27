from django import forms
from .models import tabilog as TabilogDraft

class TabilogPostingForm(forms.ModelForm):
    """ユーザー記事投稿"""

    class Meta:
        model=TabilogDraft
        fields = ('title','body')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
