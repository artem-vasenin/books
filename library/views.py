from django.db.models import Max
from django.contrib import messages
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
        messages.success(self.request, 'Книга успешно изменена!')
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
        messages.success(self.request, 'Книга успешно добавлена!')
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
        already_sent = BookPart.objects.filter(book=book, is_approved=False, author=user, part_num=book.parts_num + 1).count()
        context['content'] = BookPart.objects.filter(book=book, is_approved=True).order_by('part_num')
        context['draft'] = BookPart.objects.filter(book=book, is_approved=False, part_num=book.parts_num + 1)
        context['can_add_part'] = (
            not book.isFinished
            and book.isShared
            and (book.author.profile in user.profile.friends or book.author.pk == user.pk)
            and not already_sent
        )
        return context


class BookDeleteView(DeleteView):
    model = Book
    template_name = 'library/book-delete.html'
    success_url = reverse_lazy('library:books')


class BookAddPart(View):
    def post(self, request, pk):
        book = Book.objects.filter(pk=pk).first()
        part_text = request.POST.get('part', '').strip()

        if not part_text:
            messages.error(request, 'Текст не может быть пустым.')
            return redirect('library:book_details', pk=book.pk)

        if book.parts_num == 0:
            BookPart.objects.create(book=book, content=part_text, author=request.user, part_num=1)
        else:
            last_part = BookPart.objects.filter(book=book, is_approved=True, part_num=book.parts_num).first()
            BookPart.objects.create(
                book=book,
                content=part_text,
                author=request.user,
                part_num=book.parts_num + 1,
                parent_part=last_part,
            )
        messages.success(request, 'Контент книги успешно добавлен.')
        return redirect('library:book_details', pk=pk)

    def get(self, request, pk):
        return redirect('library:book_details', pk=pk)


class BookLock(View):
    def post(self, request, pk):
        book = Book.objects.filter(pk=pk).first()
        book.isShared = True if book.isShared == False else False
        book.save()
        messages.success(request, 'Книгу снова можно дописывать' if book.isShared else 'Книгу больше нельзя дописывать')
        return redirect('library:book_details', pk=pk)

    def get(self, request, pk):
        return redirect('library:book_details', pk=pk)


class BookFinished(View):
    def post(self, request, pk):
        book = Book.objects.filter(pk=pk).first()
        book.isFinished = not book.isFinished
        book.save()
        messages.success(request, 'Книга завершена' if book.isFinished else 'Книга еще не закончена')
        return redirect('library:book_details', pk=pk)

    def get(self, request, pk):
        return redirect('library:book_details', pk=pk)


class BookPartApprove(View):
    def post(self, request, pk, part_pk):
        book = Book.objects.filter(pk=pk).first()
        part = BookPart.objects.filter(pk=part_pk).first()
        parts_to_arch = BookPart.objects.filter(book=book, part_num=part.part_num).exclude(pk=part_pk)
        if book and part:
            book.parts_num += 1
            book.save()
            part.is_approved = True
            part.save()
            if parts_to_arch.count():
                parts_to_arch.update(is_archived=True)
            messages.success(request, 'Часть книги отмечена как продолжение, остальные перенесены в архив')
        else:
            messages.error(request, 'Ошибка подтверждения части книги')

        return redirect('library:book_details', pk=pk)

    def get(self, _, pk):
        return redirect('library:book_details', pk=pk)


class BookPartArchive(View):
    def get(self, request, pk, part_pk):
        book = Book.objects.filter(pk=pk).first()
        part = BookPart.objects.filter(pk=part_pk).first()
        parts_arch = BookPart.objects.filter(book=book, part_num=part.part_num, is_archived=True).exclude(pk=part_pk)
        if book and part and parts_arch.count():
            ctx = {'book': book, 'parts': parts_arch}
            return render(request, 'library/archive.html', context=ctx)
        else:
            messages.error(request, 'Ошибка загрузки архивов книги')
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
        messages.success(req, 'Запрос в друзья отправлен')
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
                    messages.success(req, 'Дружба прекращена')
                    res.delete()
                else:
                    messages.error(req, 'Запись о дружбе не найдена')
                    print('Запись о дружбе не найдена')
        else:
            from_profile = get_object_or_404(Profile, pk=from_pk)
            to_profile = get_object_or_404(Profile, pk=to_pk)
            try:
                result = FriendRequest.objects.filter(from_user=from_profile, to_user=to_profile).first()
                result.delete()
                messages.success(req, 'Дружба прекращена')
            except Exception as e:
                messages.error(req, 'Ошибка запроса')
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
            messages.success(req, 'Дружба подтверждена')
        except Exception as e:
            messages.error(req, 'Ошибка запроса')
            print('Ошибка:', e)

        return redirect('library:author', pk=pk)

