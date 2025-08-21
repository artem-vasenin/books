from django.shortcuts import render
from django.views.generic import View


class Index(View):
    def get(self, req):
        return render(req, 'library/home.html')

class BooksView(View):
    def get(self, req):
        return render(req, 'library/home.html')

class AuthorsView(View):
    def get(self, req):
        return render(req, 'library/home.html')

class AboutView(View):
    def get(self, req):
        return render(req, 'library/home.html')
