from django.apps import AppConfig
from django.contrib.auth import get_user_model
from django.conf import settings
import logging


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

    def ready(self):
        User = get_user_model()
        if not User.objects.exists():  # se não existir nenhum usuário
            User.objects.create_superuser(
                username=settings.USERNAME,
                email=settings.EMAIL,
                password=settings.PASSWORD
            )
            logger.info(f"Superusuário padrão criado: {settings.USERNAME} / {settings.PASSWORD}")
