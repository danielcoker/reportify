import random
import re

import nltk
from nltk import ne_chunk, word_tokenize
from nltk.tag import pos_tag

from reports.models import Report


class ReportService:
    UNKNOWN_LOCATION = "unknown"

    @staticmethod
    def submit_report(data):
        description = data.get("description")
        location = ReportService.extract_location_from_description(description) or ReportService.UNKNOWN_LOCATION

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
        location = ReportService._extract_location_from_description_with_nlp(description)

        if location == ReportService.UNKNOWN_LOCATION:
            # Todo: Add logs here.
            location = ReportService._extract_location_from_description_with_re(description)

        return location
    
    @staticmethod
    def _extract_location_from_description_with_nlp(description: str) -> str:
        # Tokenize the text into words
        words = word_tokenize(description)

        # Perform Named Entity Recognition (NER)
        tree = ne_chunk(nltk.pos_tag(words))

        location = ""

        for subtree in tree:
            if type(subtree) == nltk.Tree and subtree.label() == 'GPE':
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
        nouns = [word for word, tag in tagged_words if tag in ["NN", "NNS", "NNP", "NNPS"]]
    
        return " ".join(nouns)
