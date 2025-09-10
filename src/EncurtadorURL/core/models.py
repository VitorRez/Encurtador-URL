from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User

# Create your models here.


User = get_user_model()

class ShortURL(models.Model):
    short_code = models.TextField(unique=True)
    original_url = models.URLField()
    clicks = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    usuario = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='urls'
    )

    def __str__(self):
        return f"{self.short_code} -> {self.original_url} (criado por {self.usuario.username})"

    @property
    def usuario_email(self):
        return self.usuario.email

    @property
    def usuario_id(self):
        return self.usuario.id
