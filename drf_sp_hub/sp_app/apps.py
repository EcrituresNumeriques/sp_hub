from django.apps import AppConfig

class SpAppConfig(AppConfig):
    name = 'sp_app'

    def ready(self):
        import sp_app.signals
