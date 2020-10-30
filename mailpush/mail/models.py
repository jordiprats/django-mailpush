from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import AbstractUser
from django.utils.text import slugify
from django.db import models

import uuid

class PushPool(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=256)

class AccessToken(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    def __str__(self):
        return str(self.id)

class Subscription(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=256)

    pushpool = models.OneToOneField(PushPool, on_delete=models.CASCADE, related_name='subscriptions', null=True, blank=True)
    tokens = models.ForeignKey(AccessToken, on_delete=models.CASCADE, related_name='subscriptions', null=True, blank=True)

    def __str__(self):
        return str(self.id)

class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    slug = models.SlugField(
        default='',
        editable=False,
        max_length=100,
        unique=True,
    )
    email = models.CharField(max_length=256)
   
    subscriptions = models.ForeignKey(Subscription, on_delete=models.CASCADE, related_name='users', null=True, blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.username, allow_unicode=False)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.email

class Mail(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    subscription = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mails')


    mail_from = models.EmailField(max_length=256)
    mail_to = models.EmailField(max_length=256)
    mail_bcc = models.EmailField(max_length=256)

    mail_subject = models.CharField(max_length=256)
    mail_html = models.TextField(null=True, default=None, blank=True)
    mail_text = models.TextField(null=True, default=None, blank=True)
    autogen_text_version = models.BooleanField(default=True)

    enable_dkim = models.BooleanField(default=False)

    sent = models.BooleanField(default=False)
    bounced = models.BooleanField(default=False)
