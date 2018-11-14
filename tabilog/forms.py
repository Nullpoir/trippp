from django import forms
from .models import tabilog as TabilogDraft

OPTION_CHOICES = (
    ('title', 'タイトル'),
    ('tag', 'タグ'),
    ('author','著者名')
)

ORDER_CHOICES = (
    ("newer",'新しい順'),
    ("older",'古い順'),
    ("popular",'人気順')
)

class TabilogPostingForm(forms.ModelForm):
    """ユーザー記事投稿"""

    class Meta:
        model=TabilogDraft
        fields = ('title','body')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

class TabilogSearchForm(forms.Form):
    keywords=forms.CharField(max_length=200)
    option=forms.ChoiceField(label="検索条件",choices=OPTION_CHOICES)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        count=0;
        for field in self.fields.values():
            if count == 0:
                field.widget.attrs['class'] = 'form__text'
                count+=1
            else:
                field.widget.attrs['class'] = 'form__choice'
