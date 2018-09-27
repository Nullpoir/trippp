from django import forms

class QuestionForm(forms.Form):
    name=forms.CharField(max_length=100)
    mail=forms.EmailField()
    query=forms.CharField(widget=forms.Textarea)

    def clean_query(self):
        text=seld.cleaned_data['query']

        if (text.find("<") == -1) or (text.find(">") == -1):
            raise forms.ValidationError("<と>は使えないです...全角入力してください")

        return text
