from reports.models import Report

from core.mixins import ResponseMessageMixin

from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.permissions import AllowAny

from reports.serializers import ReportSerializer
from reports.services import ReportService


class ReportViewSet(
    ResponseMessageMixin,
    CreateModelMixin,
    ListModelMixin,
    GenericViewSet,
):
    queryset = Report.objects.all().order_by("-created_at")
    serializer_class = ReportSerializer
    permission_classes = (AllowAny,)

    def create(self, request, *args, **kwargs):
        serializer = ReportSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        report = ReportService.submit_report(serializer.validated_data)
        data = ReportSerializer(report).data

        return Response(data=data, status=status.HTTP_201_CREATED)
