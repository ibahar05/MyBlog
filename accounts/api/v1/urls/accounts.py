from django.urls import path
from .. import views
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView,
)

urlpatterns = [
    path(
        "registration/",
        views.RegistrationApiView.as_view(),
        name="registration",
    ),
    path(
        "change/password/",
        views.ChangePasswordApiView.as_view(),
        name="change-password",
    ),
    path(
        "activation/confirm/resend/",
        views.ActivationResendApiView.as_view(),
        name="confrim-resend",
    ),
    path(
        "activation/confirm/<str:token>/",
        views.ActivationApiView.as_view(),
        name="confrim",
    ),
    path(
        "jwt/create/",
        views.CustomTokenObtainPairView.as_view(),
        name="jwt-create",
    ),
    path("jwt/refresh/", TokenRefreshView.as_view(), name="jwt-refresh"),
    path("jwt/verify/", TokenVerifyView.as_view(), name="jwt-verify"),
    # path("jwt/blacklistlogout/",views.LogoutAPIView.as_view(),name="jwt-blacklist"),
]
