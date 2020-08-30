from django.apps import AppConfig


class TokenManagerConfig(AppConfig):
    name = 'token_management_system.token_manager'
    def ready(self):
        import token_management_system.token_manager.signals
