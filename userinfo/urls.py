from django.urls import path

from .views import Index, UserBooksView, FriendsView


app_name='userinfo'

urlpatterns = [
    path('', Index.as_view(), name='profile'),
    path('books/', UserBooksView.as_view(), name='user-books'),
    path('authors/', FriendsView.as_view(), name='friends'),
]