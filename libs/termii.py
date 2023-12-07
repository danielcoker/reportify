import typing as t

import requests
from django.conf import settings


def send_sms(
    phone_numbers: t.List[str],
    message: str,
    sender: str = "N-Alert",
) -> str:
    """
    Send SMS to a list of phone numbers.
    """
    url = "https://api.ng.termii.com/api/sms/send"
    payload = {
        "to": phone_numbers,
        "from": sender,
        "sms": message,
        "type": "plain",
        "channel": "generic",
        "api_key": settings.TERMII_API_KEY,
    }

    headers = {
        "Content-Type": "application/json",
    }

    if settings.APP_SERVER_ENVIRONMENT.lower() in ("production"):
        response = requests.request(
            "POST",
            url,
            headers=headers,
            json=payload,
        )

        return response.text
    else:
        return "SMS not sent in development environment."
