from django.apps import AppConfig


class AppinviteConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'appinvite'

    def ready(self):
        import appinvite.signals
