from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter
from token_management_system.token_manager.api.urls import router as token_router

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()



app_name = "api"
urlpatterns = token_router.urls
