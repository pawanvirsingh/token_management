from django.utils import timezone
from rest_framework import serializers

from token_management_system.token_manager.models import Token


class TokenSerializer(serializers.ModelSerializer):
    token = serializers.SerializerMethodField()

    class Meta:
        model = Token
        fields = ('token',)

    def get_token(self,obj):
        return obj.id

