import uuid

from django.db import models


class User(models.Model):
    id = models.UUIDField(auto_created=True, primary_key=True, default=uuid.uuid4)
    username = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)

    friends = models.ManyToManyField(to='self', blank=True, symmetrical=True)
    subscribers = models.ManyToManyField(to='self', blank=True, symmetrical=False, related_name='users')

    def __str__(self):
        return f"{self.username}"

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
