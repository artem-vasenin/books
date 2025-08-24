from django.urls import path

from .views import Index, BooksView, AuthorsView, AuthorDetailView, AboutView, BookCreateView, BookDetailsView


app_name='library'

urlpatterns = [
    path('', Index.as_view(), name='home'),
    path('books/', BooksView.as_view(), name='books'),
    path('books/create/', BookCreateView.as_view(), name='book_create'),
    path('books/<int:pk>/', BookDetailsView.as_view(), name='book_details'),
    path('authors/', AuthorsView.as_view(), name='authors'),
    path('author/<int:pk>/', AuthorDetailView.as_view(), name='author'),
    path('about/', AboutView.as_view(), name='about'),
]