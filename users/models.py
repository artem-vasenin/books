import os
from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    city = models.CharField(max_length=100, null=True, blank=True)
    about = models.TextField(null=True, blank=True)
    avatar = models.ImageField(null=True, blank=True)
    isAuthor = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        # Удаляем старую аватарку если идет замена фото
        try:
            old_avatar = Profile.objects.get(pk=self.pk).avatar
        except Profile.DoesNotExist:
            old_avatar = None

        super().save(*args, **kwargs)

        if old_avatar and old_avatar != self.avatar:
            if os.path.isfile(old_avatar.path):
                os.remove(old_avatar.path)

    def __str__(self):
        return self.user.username


class FriendRequest(models.Model):
    from_user = models.ForeignKey(Profile, related_name='from_user_field', on_delete=models.CASCADE)
    to_user = models.ForeignKey(Profile, related_name='to_user_field', on_delete=models.CASCADE)
    is_accepted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('from_user', 'to_user')

    def __str__(self):
        status = 'accepted' if self.is_accepted else 'pending'
        return f'{self.from_user} → {self.to_user} ({status})'
