from django.apps import AppConfig


class SpApiConfig(AppConfig):
    name = 'sp_api'

    def ready(self):
        import sp_api.signals
