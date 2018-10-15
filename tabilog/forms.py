from django import forms
from .models import tabilog as TabilogDraft
from .models import Images as image

FileFormset = forms.inlineformset_factory(
    TabilogDraft, image, fields='__all__',
    extra=5, max_num=10, can_delete=True
)

class TabilogPostingForm(forms.ModelForm):
    """ユーザー記事投稿"""

    class Meta:
        model=TabilogDraft
        fields = ('title','script','is_editing')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
