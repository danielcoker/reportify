from django.test import TestCase, override_settings

from reports.services import ReportService
from reports.tests.factories import CategoryFactory, ReportFactory, UserFactory


class ReportServiceTestCase(TestCase):
    @override_settings(EMAIL_BACKEND='django.core.mail.backends.smtp.EmailBackend')
    def test_notify_admins_notifies_admins(self):
        fire_category = CategoryFactory(name="Fire")
        UserFactory(
            email="testemail@test.com",
            phone="+2347xxxxxxxxx",
            is_admin=True,
            admin_category=fire_category,
        )

        report = ReportFactory(category=fire_category)

        _ = ReportService.notify_admins(report=report)
