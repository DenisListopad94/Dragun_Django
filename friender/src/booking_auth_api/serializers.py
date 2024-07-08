from ast import Dict
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import RefreshToken

class TokenObtainSerializer(TokenObtainPairSerializer):

    def validate(self, attrs) -> dict[str, str]:
        data: Dict[str, str] = super().validate(attrs)

        refresh: Token = self.get_token(self.user)
        data['refresh_token'] = str(refresh)
        data['access_token'] = str(refresh.access_token)

        data.pop('refresh', None)
        data.pop('access', None)

        return data
    
class TokenRefreshSerializer(TokenRefreshSerializer):

    def validate(self, attrs) -> dict[str, str]:
        refresh = RefreshToken(attrs['refresh'])

        data: dict[str, str] = {
            'access_token': str(refresh.access_token),
        }

        if api_settings.UPDATE_LAST_LOGIN:
            from django.contrib.auth.models import update_last_login
            update_last_login(None, refresh.user)

        return data