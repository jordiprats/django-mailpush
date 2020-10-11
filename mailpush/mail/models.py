from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import AbstractUser
from django.utils.text import slugify
from django.db import models

import uuid

class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    slug = models.SlugField(
        default='',
        editable=False,
        max_length=100,
        unique=True,
    )
    email = models.CharField(max_length=256)
    pool = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.username, allow_unicode=False)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.email

class Token(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    subscription = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tokens')

class Mail(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    subscription = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mails')

    from = models.EmailField(max_length=256)
    to = models.EmailField(max_length=256)
    bcc = models.EmailField(max_length=256)

    subject = models.CharField(max_length=256)
    text = models.TextField(null=True, default=None, blank=True)
    html = models.TextField(null=True, default=None, blank=True)