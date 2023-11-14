from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from core.mixins import ResponseMessageMixin
from users.models import User
from users.serializers import UserSerializer
from rest_framework.permissions import IsAuthenticated

class UserViewSet(ResponseMessageMixin, GenericViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)

    @action(detail=False)
    def me(self, request):
        serializer = UserSerializer(request.user, context={"request": request})

        return Response(data=serializer.data, status=status.HTTP_200_OK)
