from django.urls import path

from .views import Index, BooksView, AuthorsView, AboutView


app_name='library'

urlpatterns = [
    path('', Index.as_view(), name='home'),
    path('books/', BooksView.as_view(), name='books'),
    path('authors/', AuthorsView.as_view(), name='authors'),
    path('about/', AboutView.as_view(), name='about'),
]