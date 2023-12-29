from django.apps import AppConfig
from django.db.models.signals import post_migrate

from accounts.groups import create_groups
from accounts.permissions import create_permissions

class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'

    def ready(self):
        from accounts import signals
        post_migrate.connect(create_permissions, sender=self)
        post_migrate.connect(create_groups, sender=self)