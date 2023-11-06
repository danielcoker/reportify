from rest_framework import routers

from reports.views import ReportViewSet

router = routers.DefaultRouter(trailing_slash=False)

# Reports Routes
router.register(r"reports", ReportViewSet, basename="reports")
