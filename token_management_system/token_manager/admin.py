from django.contrib import admin

# Register your models here.
from token_management_system.token_manager.models import Pool, Token

admin.site.register(Pool)
admin.site.register(Token)
