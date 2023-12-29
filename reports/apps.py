from django.apps import AppConfig

from reportify.utils import ReportClassifierModelLoader


class ReportsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "reports"

    def ready(self):
        ReportClassifierModelLoader.load_model()
