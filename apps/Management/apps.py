from django.apps import AppConfig


class ManagementConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.Management'

    def ready(self):
        import apps.Management.signals
        import Project.signals