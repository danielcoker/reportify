import inflection
from rest_framework import renderers
from rest_framework.utils.serializer_helpers import ReturnList


class JSONRenderer(renderers.JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        status = renderer_context.get("response").status_code
        response_message = renderer_context.get("response_message", None)

        # Return an empty body for responses with 204 status code.
        if status == 204:
            return super(JSONRenderer, self).render(
                None, accepted_media_type, renderer_context
            )

        actions = {"GET": "retrieved", "POST": "created", "PUT": "updated"}

        request_method = renderer_context.get("request").method
        action = actions.get(request_method, None)
        resource_name = renderer_context.get("resource_name")

        # Pluralize resource name if the data returned is a `list` type.
        resource_name = (
            inflection.pluralize(resource_name)
            if isinstance(data, ReturnList)
            else resource_name
        )

        # Generate success message if a success message does not already exist,
        # and the action and resource name exist.
        if not response_message and action and resource_name:
            response_message = f"{resource_name} {action} successfully."

        # If the status code is 404 and the resource name exist and the error message is 'Not found.',
        # add a descriptive 'not found' message.
        if status == 404 and resource_name and data["detail"] == "Not found.":
            data["detail"] = f"{resource_name} does not exist."

        # When the 'data' data type is a rest_framework.utils.serializer_helpers.ReturnList,
        # the get attribute won't be available. This causes the 'data.get()' to raise an AttributeError
        # exception. In this case, set the message to the response_message.
        try:
            message = data.get("detail", response_message)
        except Exception:
            message = response_message

        try:
            detail_in_data = "detail" in data
        except Exception:
            detail_in_data = False

        errors = None

        # If data contains "detail" field, it means the request failed and the
        # error response message is available.
        # This error message should be returned only in the "message" field.
        if detail_in_data:
            data = None

        # If data does not contain "detail" field and the status code is 400,
        # it means there is a Validation Error.
        if not detail_in_data and status == 400:
            errors = data
            message = "Invalid input data."
            data = None

        # Construct the response data structure.
        raw_response_data = {
            "success": status < 400,
            "message": message,
            "errors": errors,
            "data": data,
        }

        # Remove response data items that have None value.
        response_data = {k: v for k, v in raw_response_data.items() if v is not None}

        response = super(JSONRenderer, self).render(
            response_data, accepted_media_type, renderer_context
        )

        return response
