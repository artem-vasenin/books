from django.shortcuts import render
from django.views.generic import View, TemplateView, DetailView

from users.models import Profile


class Index(View):
    def get(self, req):
        return render(req, 'library/home.html')


class BooksView(View):
    def get(self, req):
        return render(req, 'library/books.html')


class AuthorsView(TemplateView):
    template_name = 'library/authors.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['authors'] = Profile.objects.filter(isAuthor=True)

        return context


class AuthorDetailView(DetailView):
    model = Profile
    template_name = 'library/author.html'
    context_object_name = 'author'


class AboutView(View):
    def get(self, req):
        return render(req, 'library/about.html')
