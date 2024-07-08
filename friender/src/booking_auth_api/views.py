from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .serializers import TokenObtainSerializer, TokenRefreshSerializer

#* вьюшки на случай кастомизации работы с токенами
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = TokenObtainSerializer

class CustomTokenRefreshView(TokenRefreshView):
    serializer_class = TokenRefreshSerializer