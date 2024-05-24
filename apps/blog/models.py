from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from django.dispatch import receiver

class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

class Blog(models.Model):
    title = models.CharField(max_length=200)
    body = models.TextField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    is_private = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    passcode = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return self.title

@receiver(pre_save, sender=Blog)
def set_author(sender, instance, **kwargs):
    if not instance.author_id:
        instance.author = instance.request.user.author