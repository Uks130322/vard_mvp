from django.apps import AppConfig


class AppuserConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'appuser'

    def ready(self):
        import appinvite.signals
