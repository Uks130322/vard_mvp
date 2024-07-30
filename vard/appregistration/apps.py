from django.apps import AppConfig


class AppregistrationConfig(AppConfig):
    #default_auto_field = 'django.db.models.BigAutoField'
    name = 'appregistration'

    def ready(self):
        import appregistration.signals

