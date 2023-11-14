from django.contrib import admin

from reports.models import Category, Report


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
    )


class ReportAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "category",
        "location",
        "status",
        "description",
        "created_at",
    )


admin.site.register(Category, CategoryAdmin)
admin.site.register(Report, ReportAdmin)
