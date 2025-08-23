from django import forms

class ProfileUpdateForm(forms.Form):
    first_name = forms.CharField(
        max_length=150,
        required=False,
        label='Имя',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Имя'
        })
    )
    last_name = forms.CharField(
        max_length=150,
        required=False,
        label='Фамилия',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Фамилия'
        })
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите email'
        })
    )

    city = forms.CharField(
        max_length=100,
        required=False,
        label='Город',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Город'
        })
    )
    about = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'О себе'
        }),
        required=False,
        label='О себе',
    )
    avatar = forms.ImageField(
        required=False,
        label='Аватар',
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'accept': 'image/*',
        }),
    )
    isAuthor = forms.BooleanField(
        required=False,
        label='Автор',
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input',
        })
    )