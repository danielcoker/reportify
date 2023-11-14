from rest_framework.routers import SimpleRouter

from authentication.views import AuthViewSet

router = SimpleRouter()


router.register(
    r"users/auth",
    AuthViewSet,
    basename="auth",
)
