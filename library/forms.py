from django import forms
from tinymce.widgets import TinyMCE
from django.contrib.auth.models import User

class BookCreateForm(forms.Form):
    title = forms.CharField(
        max_length=250,
        required=True,
        label='Заголовок',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Заголовок'
        })
    )
    description = forms.CharField(
        widget=TinyMCE(attrs={'class': 'form-control', 'cols': 80, 'rows': 30}),
        required=False,
        label='Описание',
    )
    content = forms.CharField(
        widget=TinyMCE(attrs={'class': 'form-control', 'cols': 80, 'rows': 30}),
        required=True,
        label='Текст главы'
    )
    # author = forms.ModelChoiceField(
    #     queryset=User.objects.filter(profile__isAuthor=True),
    #     required=True,
    #     label='Автор',
    #     widget=forms.Select(attrs={'class': 'form-control'})
    # )
    image = forms.ImageField(
        required=False,
        label='Изображение',
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'accept': 'image/*',
        }),
    )

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['author'].label_from_instance = lambda obj: obj.username