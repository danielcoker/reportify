import random
import re
import typing as t

import nltk
from django.conf import settings
from django.core.mail import send_mail
from django.db import transaction
from nltk import ne_chunk, word_tokenize
from nltk.tag import pos_tag
from rest_framework.exceptions import ValidationError

from libs import termii
from reportify.utils import generate_random_string
from reports.models import Category, Report
from users.models import User


class ReportService:
    UNKNOWN_LOCATION = "unknown"

    @staticmethod
    def get_report(id: str) -> Report:
        """
        Fetch a report by its id.
        """
        try:
            report = Report.objects.get(id=id)
        except Report.DoesNotExist:
            raise ValidationError("Report does not exist.")

        return report

    @staticmethod
    def get_reports(user: t.Optional[User] = None) -> t.List[Report]:
        """
        Fetch all reports for a particular user based on their role.
        Only perform this filtering if the user object passed is an
        instance of User and the user is an admin.
        """
        if isinstance(user, User) and user.is_admin is True:
            return Report.objects.filter(category=user.admin_category)
        else:
            return Report.objects.all()

    @staticmethod
    def acknowledge_report(id: str) -> Report:
        """
        Acknowledge a report.
        """
        report = ReportService.get_report(id=id)

        if report.status != Report.Status.OPEN:
            raise ValidationError("Report is not open.")

        report.status = Report.Status.IN_PROGRESS
        report.save(update_fields=["status", "updated_at"])

        # TODO: Notify user that their report has been acknowledged.

        return report

    @staticmethod
    def resolve_report(id: str) -> Report:
        """
        Resolve a report.
        """
        report = ReportService.get_report(id=id)

        if report.status not in [Report.Status.OPEN, Report.Status.IN_PROGRESS]:
            raise ValidationError("Report is not open or in-progress.")

        report.status = Report.Status.RESOLVED
        report.save(update_fields=["status", "updated_at"])

        # TODO: Notify user that their report has been resolved.

        return report

    @staticmethod
    def change_report_category(id: str, category_id: int) -> Report:
        """
        Change the category of a report.

        This should cater for instances where the system misclassifies the incident category,
        or if the admin decides to reclassify the incident category.
        """
        report = ReportService.get_report(id=id)
        category = ReportService.get_category(id=category_id)

        report.category = category
        report.save(update_fields=["category", "updated_at"])

        return report

    @staticmethod
    def submit_report(data):
        from authentication.services import AuthenticationService

        description = data.get("description")
        name = data.get("name")
        phone = data.get("phone")
        location = (
            ReportService.extract_location_from_description(description)
            or ReportService.UNKNOWN_LOCATION
        )

        # Todo: Use ML algorithm to predict the incident category.
        category_id = random.randint(1, 3)

        # Create user.
        with transaction.atomic():
            try:
                user = User.objects.get(phone=phone)
            except User.DoesNotExist:
                email = f"gen_{phone}@reportify.io"
                password = generate_random_string(8)

                full_name_parts = name.split(" ")
                first_name, *last_name = full_name_parts

                user_data = {
                    "first_name": first_name,
                    "last_name": " ".join(last_name),
                    "email": email,
                    "phone": phone,
                    "password": password,
                    "is_active": False,
                }
                user = AuthenticationService.create_user(**user_data)

            report = Report.objects.create(
                description=description,
                location=location,
                category_id=category_id,
                user=user,
            )

        ReportService.notify_admins(report=report)

        return report

    @staticmethod
    def notify_admins(report: Report):
        """
        Notify admins of a new report.
        """
        admin_users_for_category = User.objects.values_list("phone", "email").filter(
            admin_category_id=report.category_id,
            is_admin=True,
        )

        admin_phones = []
        admin_emails = []

        for phone, email in admin_users_for_category:
            admin_phones.append(phone)
            admin_emails.append(email)

        try:
            ReportService._send_admin_sms_notification(report, set(admin_phones))
            ReportService._send_admin_email_notification(report, set(admin_emails))
        except Exception as e:
            print(f"An error occurred while sending admin notifications. {e}")
            return False

        return True

    @staticmethod
    def _send_admin_sms_notification(report: Report, phones: t.List[str]):
        """
        Send SMS notification to admins.
        """
        message = "A new incident report has just been submitted. Login to your dashboard to view the details."

        termii.send_sms(phone_numbers=list(phones), message=message)

    @staticmethod
    def _send_admin_email_notification(report: Report, emails: t.List[str]):
        """
        Send email notification to admins.
        """
    
        message = f"""
            Hello,

            A new incident report has just been submitted. Find the details below:

            Description: {report.description}
            Location: {report.location}
            Category: {report.category.name}
            Date: {report.created_at.strftime("%d %b, %I:%M %p")}

            Regards,
            Reportify
        """
        
        if settings.APP_SERVER_ENVIRONMENT.lower() in ("production"):
            send_mail(
                "[NEW] Reportify - New Incident Report",
                message,
                settings.DEFAULT_FROM_EMAIL,
                list(emails),
                fail_silently=False,
            )
        else:
            print(message)

    @staticmethod
    def extract_location_from_description(description: str) -> str:
        """
        Extract the location from the incident description.

        This attempts to extract the incident location from the description using an NLP technique first,
        if it still returns "unknown", use Regular Expressions as a fallback.

        A possible improvement is when Google Maps API is available, we can use it to geocode the location,
        and if we are still unable to retrieve the location, we can then use the other techniques as fallbacks.
        """
        # Todo: Add logs here.
        location = ReportService._extract_location_from_description_with_nlp(
            description
        )

        if location == ReportService.UNKNOWN_LOCATION:
            # Todo: Add logs here.
            location = ReportService._extract_location_from_description_with_re(
                description
            )

        return location

    @staticmethod
    def _extract_location_from_description_with_nlp(description: str) -> str:
        # Tokenize the text into words
        words = word_tokenize(description)

        # Perform Named Entity Recognition (NER)
        tree = ne_chunk(nltk.pos_tag(words))

        location = ""

        for subtree in tree:
            if type(subtree) == nltk.Tree and subtree.label() == "GPE":
                location = " ".join([word for word, tag in subtree.leaves()])

        if location == "":
            location = ReportService.UNKNOWN_LOCATION

        normalized_location = ReportService.normalize_location(location)

        return normalized_location

    @staticmethod
    def _extract_location_from_description_with_re(description: str) -> str:
        """
        Extract the location from the incident description using Regular Expressions.
        """
        match = re.search(
            r"\b(?:on|in|near|at)\s+(\w+\s*\w*)\b",
            description,
            re.IGNORECASE,
        )

        if match:
            location = match.group(1)
            location = ReportService.filter_nouns(location) or location
        else:
            location = ReportService.UNKNOWN_LOCATION

        normalized_location = ReportService.normalize_location(location)

        return normalized_location

    @staticmethod
    def normalize_location(location: str) -> str:
        """
        Convert location to lowercase and remove leading/trailing whitespaces
        """
        return location.lower().strip()

    @staticmethod
    def filter_nouns(text):
        words = word_tokenize(text)
        tagged_words = pos_tag(words)
        nouns = [
            word for word, tag in tagged_words if tag in ["NN", "NNS", "NNP", "NNPS"]
        ]

        return " ".join(nouns)

    @staticmethod
    def get_category(*, id: int = None, name: str = None) -> Category:
        """
        Fetch a category by its id.
        """
        if not id and not name:
            raise ValidationError("Either id or name is required.")

        if id and name:
            raise ValidationError("Only one of id or name is allowed.")

        if id:
            return ReportService._get_category_by_id(id)

        if name:
            return ReportService._get_category_by_name(name)

    @staticmethod
    def _get_category_by_id(id: int) -> Category:
        """
        Fetch a category by its id.
        """
        try:
            category = Category.objects.get(id=id)
        except Category.DoesNotExist:
            raise ValidationError("Category does not exist.")

        return category

    @staticmethod
    def _get_category_by_name(name: str) -> Category:
        """
        Fetch a category by its name.
        """
        try:
            category = Category.objects.get(name=name)
        except Category.DoesNotExist:
            raise ValidationError("Category does not exist.")

        return category
