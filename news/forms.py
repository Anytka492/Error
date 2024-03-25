from django import forms
from django.core.exceptions import ValidationError
from .models import Post


class PostForm(forms.ModelForm):
    title = forms.CharField(min_length=10, max_length=100, label='Заголовок')
    text = forms.CharField(widget=forms.Textarea({'rows': '5'}), label='Содержимое', min_length=200)
    class Meta:
        model = Post
        fields = [
            'title',
            'text',
            'author',
            'categoryType',
            'rating'
        ]

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get("title")
        text = cleaned_data.get("text")

        if title == text:
            raise ValidationError(
                "Содержание не должно быть идентично заголовку."
            )

        return cleaned_data

    def clean_title(self):
        title = self.cleaned_data["title"]
        if title[0].islower():
            raise ValidationError(
                "Заголовок должно начинаться с заглавной буквы"
            )
        return title

    def clean_text(self):
        text = self.cleaned_data["text"]
        if text[0].islower():
            raise ValidationError(
                "Содержание должно начинаться с заглавной буквы"
            )
        return text