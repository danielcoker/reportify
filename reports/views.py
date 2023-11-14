from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from core.mixins import ResponseMessageMixin
from core.permissions import IsEmergencyServiceAdmin
from reports.models import Report
from reports.serializers import ChangeCategorySerializer, ReportSerializer, SubmitReportSerializer
from reports.services import ReportService


class ReportViewSet(
    ResponseMessageMixin,
    CreateModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
    GenericViewSet,
):
    serializer_class = ReportSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        user = self.request.user
        return ReportService.get_reports(user)

    def create(self, request, *args, **kwargs):
        serializer = SubmitReportSerializer(data=request.data)
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

    @action(
        detail=True,
        methods=["POST"],
        url_path="change-category",
        url_name="change-category",
        permission_classes=(
            IsAuthenticated,
            IsEmergencyServiceAdmin,
        ),
    )
    def change_report_category(self, request, pk=None):
        serializer = ChangeCategorySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        category_id = serializer.validated_data.get("category_id")

        report = ReportService.change_report_category(pk, category_id)
        data = ReportSerializer(report).data

        self.response_message = "Report category changed successfully."

        return Response(data=data, status=status.HTTP_200_OK)
