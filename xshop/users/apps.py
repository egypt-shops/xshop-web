from django.apps import AppConfig


class UsersConfig(AppConfig):
    name = "xshop.users"

    def ready(self) -> None:
        import xshop.users.signals  # noqa
