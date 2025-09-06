from django.urls import path

from .views import (
    Index, BooksView, AuthorsView, AuthorDetailView, AboutView, BookCreateView, BookDetailsView, BookLock,
    SendFriendRequestView, RemoveFriendView, AddFriendView, BookEditView, BookAddPart, BookDeleteView, BookFinished,
)


app_name='library'

urlpatterns = [
    path('', Index.as_view(), name='home'),
    path('books/', BooksView.as_view(), name='books'),
    path('books/create/', BookCreateView.as_view(), name='book_create'),
    path('books/<int:pk>/', BookDetailsView.as_view(), name='book_details'),
    path('books/<int:pk>/lock/', BookLock.as_view(), name='book_lock'),
    path('books/<int:pk>/finished/', BookFinished.as_view(), name='book_finished'),
    path('books/edit/<int:pk>/', BookEditView.as_view(), name='book_edit'),
    path('books/delete/<int:pk>/', BookDeleteView.as_view(), name='book_delete'),
    path('books/<int:pk>/add/', BookAddPart.as_view(), name='book_add'),
    path('authors/', AuthorsView.as_view(), name='authors'),
    path('author/<int:pk>/', AuthorDetailView.as_view(), name='author'),
    path('author/friend/<int:pk>/', SendFriendRequestView.as_view(), name='to_friends'),
    path('author/friend/add/<int:pk>/', AddFriendView.as_view(), name='add_friend'),
    path('author/delete/<int:from_pk>/<int:to_pk>/<int:page_pk>/', RemoveFriendView.as_view(), name='remove_friend'),
    path('about/', AboutView.as_view(), name='about'),
]