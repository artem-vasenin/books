from django.db.models import Max
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.db.models import Prefetch
from django.contrib.auth.models import User
from django.views.generic.edit import FormView
from django.shortcuts import render, get_object_or_404
from django.views.generic import View, TemplateView, DetailView, DeleteView

from .forms import BookCreateForm
from .models import Book, BookPart
from users.models import Profile, FriendRequest
from users.views import IsUserMixin, IsAuthorMixin


class Index(View):
    def get(self, req):
        books = Book.objects.all()
        authors = Profile.objects.filter(isAuthor=True)
        users = Profile.objects.filter(isAuthor=False)
        return render(req, 'library/home.html', {'books': books, 'authors': authors, 'users': users})


class BooksView(TemplateView):
    template_name = 'library/books.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['books'] = (
            Book.objects
            .select_related('author')  # автор тянется JOIN-ом
            .prefetch_related('bookpart_set')  # части книги тянутся отдельным запросом
        )

        return context


class BookEditView(FormView):
    template_name = 'library/book-edit.html'
    form_class = BookCreateForm
    success_url = reverse_lazy('library:books')

    def get_initial(self):
        book = Book.objects.filter(pk=self.kwargs['pk']).first()
        return {
            'title': book.title,
            'description': book.description,
            'image': book.image,
        }

    def form_valid(self, form):
        book = Book.objects.filter(pk=self.kwargs['pk']).first()
        book.title = form.cleaned_data['title']
        book.description = form.cleaned_data['description']
        book.image = form.cleaned_data['image']
        book.save()
        return super().form_valid(form)


class BookCreateView(IsAuthorMixin, FormView):
    template_name = 'library/book-create.html'
    form_class = BookCreateForm
    success_url = reverse_lazy('library:books')

    def form_valid(self, form):
        current_user = self.request.user
        Book.objects.create(
            title=form.cleaned_data['title'],
            author=current_user,
            description=form.cleaned_data['description'],
            image=form.cleaned_data['image'],
        )
        return super().form_valid(form)


class AuthorsView(TemplateView):
    template_name = 'library/authors.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['authors'] = Profile.objects.filter(isAuthor=True)
        context['authors'] = (
            User.objects
            .filter(profile__isAuthor=True)
            .prefetch_related(
                Prefetch(
                    'book_set',
                    queryset=Book.objects.select_related('author'),  # подхватим и автора книги
                    to_attr='books'  # сохраним в кастомное свойство, чтобы в шаблоне было author.books
                )
            )
        )

        return context


class BookDetailsView(DetailView):
    model = Book
    template_name = 'library/book-details.html'
    context_object_name = 'book'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        book = context['book']
        user = self.request.user
        context['can_add_part'] = not book.isFinished and book.isShared and (book.author.profile in user.profile.friends or book.author.pk == user.pk)
        return context


class BookDeleteView(DeleteView):
    model = Book
    template_name = 'library/book-delete.html'
    success_url = reverse_lazy('library:books')


class BookAddPart(View):
    def post(self, request, pk):
        book = Book.objects.filter(pk=pk).first()
        max_num = BookPart.objects.filter(book=book).aggregate(Max('part_num'))['part_num__max']
        last_part = BookPart.objects.filter(book=book, is_approved=True, part_num=max_num)
        return redirect('library:book_details', pk=pk)

    def get(self, request, pk):
        return redirect('library:book_details', pk=pk)


class BookLock(View):
    def post(self, request, pk):
        book = Book.objects.filter(pk=pk).first()
        book.isShared = True if book.isShared == False else False
        book.save()
        return redirect('library:book_details', pk=pk)

    def get(self, request, pk):
        return redirect('library:book_details', pk=pk)


class BookFinished(View):
    def post(self, request, pk):
        book = Book.objects.filter(pk=pk).first()
        book.isFinished = not book.isFinished
        book.save()
        return redirect('library:book_details', pk=pk)

    def get(self, request, pk):
        return redirect('library:book_details', pk=pk)


class AuthorDetailView(DetailView):
    model = Profile
    template_name = 'library/author.html'
    context_object_name = 'author'


class AboutView(TemplateView):
    template_name = 'library/about.html'


class SendFriendRequestView(IsUserMixin, View):
    def post(self, req, pk):
        to_profile = get_object_or_404(Profile, pk=pk)
        FriendRequest.objects.get_or_create(from_user=req.user.profile, to_user=to_profile)
        return redirect('library:author', pk=pk)


class RemoveFriendView(IsUserMixin, View):
    def post(self, req, from_pk, to_pk, page_pk):
        if not from_pk and not to_pk and page_pk:
            my_profile = get_object_or_404(Profile, pk=req.user.profile.pk)
            friend_profile = get_object_or_404(Profile, pk=page_pk)
            res = FriendRequest.objects.filter(from_user=my_profile, to_user=friend_profile).first()
            if res:
                res.delete()
            else:
                res = FriendRequest.objects.filter(from_user=friend_profile, to_user=my_profile).first()
                if res:
                    res.delete()
                else:
                    print('Запись о дружбе не найдена')
        else:
            from_profile = get_object_or_404(Profile, pk=from_pk)
            to_profile = get_object_or_404(Profile, pk=to_pk)
            try:
                result = FriendRequest.objects.filter(from_user=from_profile, to_user=to_profile).first()
                result.delete()
            except Exception as e:
                print('Ошибка:', e)
        return redirect('library:author', pk=page_pk)


class AddFriendView(IsUserMixin, View):
    def post(self, req, pk):
        from_profile = get_object_or_404(Profile, pk=pk)
        to_profile = get_object_or_404(Profile, pk=req.user.profile.pk)
        result = FriendRequest.objects.filter(from_user=from_profile, to_user=to_profile).first()
        try:
            result.accepted = True
            result.save()
        except Exception as e:
            print('Ошибка:', e)

        return redirect('library:author', pk=pk)

