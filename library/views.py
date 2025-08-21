from django.shortcuts import render
from django.views.generic import View


class Index(View):
    def get(self, req):
        return render(req, 'library/index.html')
