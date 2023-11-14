import random
import re
import typing as t

import nltk
from nltk import ne_chunk, word_tokenize
from nltk.tag import pos_tag
from rest_framework.exceptions import ValidationError

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
    def submit_report(data):
        description = data.get("description")
        location = (
            ReportService.extract_location_from_description(description)
            or ReportService.UNKNOWN_LOCATION
        )

        # Todo: Use ML algorithm to predict the incident category.
        category_id = random.randint(1, 3)

        report = Report.objects.create(
            description=description,
            location=location,
            category_id=category_id,
        )

        return report

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
