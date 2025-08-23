from users.models import Profile

def menu_data(request):
    return {
        'authors_count': Profile.objects.filter(isAuthor=True).count(),
        'books_count': 0,
    }