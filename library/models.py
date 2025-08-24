from django.db import models
from tinymce.models import HTMLField

from users.models import Profile


class Book(models.Model):
    title = models.CharField(max_length=250, unique=True)
    author = models.ForeignKey(Profile, on_delete=models.DO_NOTHING)
    description = HTMLField(null=True, blank=True)
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.title
