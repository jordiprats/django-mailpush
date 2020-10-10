from django.db import models

# Create your models here.

class Mail(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    from = models.EmailField(max_length=256)
    to = models.EmailField(max_length=256)
    bcc = models.EmailField(max_length=256)

    subject = models.CharField(max_length=256)
    text = models.TextField(null=True, default=None, blank=True)
    html = models.TextField(null=True, default=None, blank=True)