import os
from django.db import models
from tinymce.models import HTMLField
from django.contrib.auth.models import User


class Book(models.Model):
    title = models.CharField(max_length=250, unique=True)
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    description = HTMLField(null=True, blank=True)
    image = models.ImageField(null=True, blank=True, upload_to='books/')
    parts_num = models.PositiveIntegerField(default=0)
    isFinished = models.BooleanField(default=False)
    isShared = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        try:
            old_img = Book.objects.get(pk=self.pk).image
        except Book.DoesNotExist:
            old_img = None

        super().save(*args, **kwargs)

        if old_img and old_img != self.image:
            if os.path.isfile(old_img.path):
                os.remove(old_img.path)


class BookPart(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    parent_part = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING)
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
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('part', 'user')

    def __str__(self):
        return f'part: {self.part.part_num} - {self.user}'
