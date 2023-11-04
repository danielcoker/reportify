class ResponseMessageMixin:
    """
    Adds a resource name and response message to the renderer context to be used by
    a renderer to display response messages.
    """

    resource_name = None
    response_message = None

    def get_renderer_context(self):
        context = super().get_renderer_context()

        if not self.resource_name:
            try:
                self.resource_name = (
                    type(self.get_queryset()[0]).__name__
                    if hasattr(self, "get_queryset")
                    else None
                )
            except IndexError:
                # If the queryset returns an empty list,
                # set `response_message` to 'No records found.'
                self.response_message = "No records found."
            except:  # NOQA
                # If an error is raised, fail silently and move on.
                pass

        context["resource_name"] = self.resource_name
        context["response_message"] = self.response_message

        return context
