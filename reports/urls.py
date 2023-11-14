from rest_framework.routers import SimpleRouter

from reports.views import ReportViewSet

router = SimpleRouter()


router.register(
    r"reports",
    ReportViewSet,
    basename="reports",
)
