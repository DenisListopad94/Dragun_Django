from django.urls import URLPattern, include, path
from .views import CustomTokenObtainPairView, CustomTokenRefreshView


urlpatterns: list[URLPattern] = [
    path('token', CustomTokenObtainPairView.as_view(), name='token_obtain'),
    path('token/refresh', CustomTokenRefreshView.as_view(), name='token_refresh'),
]
