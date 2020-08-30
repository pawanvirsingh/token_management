from rest_framework.routers import SimpleRouter

from token_management_system.token_manager.api import views


router = SimpleRouter()

router.register(r'token', views.TokenViewset, basename='get-hosted-url')
