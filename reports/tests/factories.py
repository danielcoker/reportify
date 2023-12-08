import typing as t
import factory
from django.contrib.auth import get_user_model

from reports.models import Category, Report


class UserFactory(factory.django.DjangoModelFactory):
    username = factory.Faker("user_name")
    email = factory.Faker("email")
    first_name = factory.Faker("name")
    last_name = factory.Faker("name")
    phone = factory.Sequence(lambda n: f"0801234567{n}")
    password = factory.PostGenerationMethodCall("set_password", "password")

    class Meta:
        model = get_user_model()
        django_get_or_create = ["username"]


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    name = factory.Faker("random_element", elements=[
        "Fire",
        "Crime",
        "Health",
    ])


class ReportFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Report

    category = factory.SubFactory("reports.tests.factories.CategoryFactory")
    description = "Test description"
    location = "Test location"
    status = Report.Status.OPEN
    user = factory.SubFactory("reports.tests.factories.UserFactory")
