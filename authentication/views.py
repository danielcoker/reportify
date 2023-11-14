from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from authentication.serializers import (
    SignUpSerializer,
    SignInSerializer,
)
from authentication.services import AuthenticationService
from core.mixins import ResponseMessageMixin
from users.models import User


class AuthViewSet(ResponseMessageMixin, ViewSet):
    permission_classes = (AllowAny,)

    @action(
        methods=["POST"],
        detail=False,
        url_path="sign-up",
        url_name="sign-up",
    )
    def sign_up(self, request, **kwargs):
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = AuthenticationService.create_user(**serializer.data)
        data = AuthenticationService.make_auth_response_data(user=user)

        self.response_message = "User signed up successfully."

        return Response(data, status=status.HTTP_201_CREATED)

    @action(
        methods=["POST"],
        detail=False,
        url_path="sign-in",
        url_name="sign-in",
    )
    def sign_in(self, request, **kwargs):
        serializer = SignInSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = AuthenticationService.sign_in(**serializer.data)
        data = AuthenticationService.make_auth_response_data(user=user)

        self.response_message = "User signed in successfully."

        return Response(data, status=status.HTTP_200_OK)
