from django.apps import AppConfig


class ManagementConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Management'

    def ready(self):
        import Management.signals
        import Project.signals