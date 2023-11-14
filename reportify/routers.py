from rest_framework import routers

from authentication.urls import router as auth_router
from reports.urls import router as report_router
from users.urls import router as user_router

v1_router = routers.SimpleRouter(trailing_slash=False)

v1_router.registry.extend(auth_router.registry)
v1_router.registry.extend(report_router.registry)
v1_router.registry.extend(user_router.registry)
