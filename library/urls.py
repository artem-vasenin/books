from django.urls import path

from .views import (
    Index, BooksView, AuthorsView, AuthorDetailView, AboutView, BookCreateView, BookDetailsView,
    SendFriendRequestView, RemoveFriendView, AddFriendView, BookEditView,
)


app_name='library'

urlpatterns = [
    path('', Index.as_view(), name='home'),
    path('books/', BooksView.as_view(), name='books'),
    path('books/create/', BookCreateView.as_view(), name='book_create'),
    path('books/<int:pk>/', BookDetailsView.as_view(), name='book_details'),
    path('books/edit/<int:pk>/', BookEditView.as_view(), name='book_edit'),
    path('authors/', AuthorsView.as_view(), name='authors'),
    path('author/<int:pk>/', AuthorDetailView.as_view(), name='author'),
    path('author/friend/<int:pk>/', SendFriendRequestView.as_view(), name='to_friends'),
    path('author/friend/add/<int:pk>/', AddFriendView.as_view(), name='add_friend'),
    path('author/delete/<int:from_pk>/<int:to_pk>/<int:page_pk>/', RemoveFriendView.as_view(), name='remove_friend'),
    path('about/', AboutView.as_view(), name='about'),
]