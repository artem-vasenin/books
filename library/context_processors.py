from users.models import Profile
from .models import Book

def menu_data(request):
    return {
        'authors_count': Profile.objects.filter(isAuthor=True).count(),
        'friends_count': request.user.profile.friends.count(),
        'books_count': Book.objects.all().count(),
    }