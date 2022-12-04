from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save

from rest_framework.authtoken.models import Token


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

class User(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=50, unique=True)

    def as_dict(self):
        obj_d = {
            "id": self.id,
            "email": self.email,
            "username": self.username,
            "first_name": self.first_name,
            "last_name": self.last_name,
        }
        return obj_d



class Group(models.Model):
    name = models.CharField(max_length=256, unique=True)
    members = models.ManyToManyField(User, blank=True, related_name='group_members')
    created_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)


class GroupMessage(models.Model):
    message = models.CharField(max_length=1000)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    liked_by = models.ManyToManyField(User, blank=True, related_name='group_messages')
    created_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
