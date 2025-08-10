from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import View

class LoginView(View):
    def get(self, req):
        return render(req, 'users/login-form.html')

class RegView(View):
    def get(self, req):
        return render(req, 'users/register-form.html')

class LogoutView(View):
    def get(self, req):
        return HttpResponse('Logout')
