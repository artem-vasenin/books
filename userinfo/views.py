from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic import View, FormView
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import ProfileUpdateForm


class Index(LoginRequiredMixin, FormView):
    template_name = 'userinfo/profile.html'
    form_class = ProfileUpdateForm
    success_url = reverse_lazy('userinfo:profile')

    def get_initial(self):
        """Заполняем форму начальными данными"""
        user = self.request.user
        profile = user.profile

        return {
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'city': profile.city,
            'about': profile.about,
            'avatar': profile.avatar,
            'isAuthor': profile.isAuthor,
        }

    def form_valid(self, form):
        """Сохраняем данные из формы в User и Profile"""
        user = self.request.user
        profile = user.profile

        # обновляем User
        user.first_name = form.cleaned_data['first_name']
        user.last_name = form.cleaned_data['last_name']
        user.email = form.cleaned_data['email']
        user.save()

        # обновляем Profile
        profile.city = form.cleaned_data['city']
        profile.about = form.cleaned_data['about']
        profile.isAuthor = form.cleaned_data['isAuthor']

        if form.cleaned_data['avatar']:
            profile.avatar = form.cleaned_data['avatar']

        profile.save()

        messages.success(self.request, 'Данные обновлены!')
        return super().form_valid(form)


class FriendsView(View):
    def get(self, req):
        return render(req, 'userinfo/friends.html')


class UserBooksView(View):
    def get(self, req):
        return render(req, 'userinfo/books.html')