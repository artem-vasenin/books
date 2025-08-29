from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic import View, FormView
from django.contrib.auth.mixins import LoginRequiredMixin

from users.models import FriendRequest, Profile
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


class FriendsView(LoginRequiredMixin, View):
    def get(self, req):
        def friends():
            # accepted запросы где я участвую
            sent = FriendRequest.objects.filter(from_user=req.user.profile, accepted=True)
            sent_res = [{'user': i.to_user, 'date': i.created_at} for i in sent]
            received = FriendRequest.objects.filter(to_user=req.user.profile, accepted=True)
            received_res = [{'user': i.from_user, 'date': i.created_at} for i in received]
            return list(sent_res) + list(received_res)

        def friends_request_from_me():
            # accepted запросы где я запросил
            res = FriendRequest.objects.filter(from_user=req.user.profile, accepted=False)
            return [{'user': i.to_user, 'date': i.created_at} for i in res]

        def friends_request_to_me():
            # accepted запросы где меня запросили
            res = FriendRequest.objects.filter(to_user=req.user.profile, accepted=False)
            return [{'user': i.from_user, 'date': i.created_at} for i in res]

        return render(req, 'userinfo/friends.html', {
            'req_approved': friends(),
            'req_my': friends_request_from_me(),
            'req_to_me': friends_request_to_me(),
        })


class UserBooksView(LoginRequiredMixin, View):
    def get(self, req):
        return render(req, 'userinfo/books.html')