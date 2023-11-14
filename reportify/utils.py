import random
import string
from collections import OrderedDict

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class CustomPageNumberPagination(PageNumberPagination):
    max_page_size = 20
    page_size_query_param = "page_size"

    def get_paginated_response(self, data):
        return Response(
            OrderedDict(
                [
                    ("count", self.page.paginator.count),
                    ("next", self.get_next_link()),
                    ("previous", self.get_previous_link()),
                    (
                        "current_page",
                        self.get_page_number(
                            self.request,
                            self.page.paginator,
                        ),
                    ),
                    ("total_pages", self.page.paginator.num_pages),
                    ("results", data),
                ]
            )
        )



def generate_random_string(string_length: int = 5) -> str:
    """
    Generate random string.
    """
    random_string = "".join(
        random.choices(
            string.ascii_uppercase + string.digits,
            k=string_length,
        )
    )

    return random_string


def generate_random_numbers(number_length: int = 5) -> str:
    """
    Generate random numbers.
    """
    random_numbers = "".join(
        random.choices(
            string.digits,
            k=number_length,
        )
    )

    return random_numbers