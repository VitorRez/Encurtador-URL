from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class ShortURL(models.Model):
    short_code = models.CharField(max_length=10, unique=True)
    original_url = models.URLField()
    clicks = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.short_code} -> {self.original_url}"
