from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from core.mixins import ResponseMessageMixin
from core.permissions import IsEmergencyServiceAdmin
from reports.models import Report
from reports.serializers import ReportSerializer
from reports.services import ReportService


class ReportViewSet(
    ResponseMessageMixin,
    CreateModelMixin,
    ListModelMixin,
    GenericViewSet,
):
    serializer_class = ReportSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        user = self.request.user
        return ReportService.get_reports(user)

    def create(self, request, *args, **kwargs):
        serializer = ReportSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        report = ReportService.submit_report(serializer.validated_data)
        data = ReportSerializer(report).data

        return Response(data=data, status=status.HTTP_201_CREATED)

    @action(
        detail=True,
        methods=["POST"],
        url_path="acknowledge",
        url_name="acknowledge",
        permission_classes=(
            IsAuthenticated,
            IsEmergencyServiceAdmin,
        ),
    )
    def acknowledge_report(self, request, pk=None):
        report = ReportService.acknowledge_report(pk)
        data = ReportSerializer(report).data

        self.response_message = "Report acknowledged successfully."

        return Response(data=data, status=status.HTTP_200_OK)

    @action(
        detail=True,
        methods=["POST"],
        url_path="resolve",
        url_name="resolve",
        permission_classes=(
            IsAuthenticated,
            IsEmergencyServiceAdmin,
        ),
    )
    def resolve_report(self, request, pk=None):
        report = ReportService.resolve_report(pk)
        data = ReportSerializer(report).data

        self.response_message = "Report resolved successfully."

        return Response(data=data, status=status.HTTP_200_OK)
