from django.db import models
from tinymce.models import HTMLField

from users.models import Profile


class Book(models.Model):
    title = models.CharField(max_length=250, unique=True)
    author = models.ForeignKey(Profile, on_delete=models.DO_NOTHING)
    description = HTMLField(null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    parts_num = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class BookPart(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    parent_part = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    author = models.ForeignKey(Profile, on_delete=models.DO_NOTHING)
    content = HTMLField()
    part_num = models.PositiveIntegerField(default=0)
    is_approved = models.BooleanField(default=False)
    is_archived = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.book.title} - part {self.part_num} ({self.author if self.author else "---"})'


class Vote(models.Model):
    part = models.ForeignKey(BookPart, on_delete=models.CASCADE)
    user = models.ForeignKey(Profile, on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('part', 'user')

    def __str__(self):
        return f'part: {self.part.part_num} - {self.user}'
