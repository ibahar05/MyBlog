from rest_framework.response import Response
from rest_framework import generics
from rest_framework import status
from .serializers import (
    RegistrationSerializer,
    CustomTokenObtainPairSerilaizer,
    ChangePassowrdSerializer,
    ProfileSerializer,
    ActivationResendSerializer,
)
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from ...models import Profile
from django.shortcuts import get_object_or_404
from mail_templated import EmailMessage
from ..utils import EmailThreading
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
import jwt
from jwt.exceptions import ExpiredSignatureError, InvalidSignatureError
from django.conf import settings

User = get_user_model()


class RegistrationApiView(generics.GenericAPIView):
    serializer_class = RegistrationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            email = serializer.validated_data["email"]
            data = {"email": email}
            user_obj = get_object_or_404(User, email=email)
            token = self.get_token_for_users(user_obj)
            email_obj = EmailMessage(
                "email/activation_email.tpl",
                {"token": token},
                "admin@admin.com",
                to=[email],
            )
            EmailThreading(email_obj).start()
            return Response(data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_token_for_users(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)


# -----------------------------------------------------------------------------------------------------------

# class CustomObtainAuthToken(ObtainAuthToken):

#     serializer_class = CustomAuthTokenSerializer

#     def post(self, request, *args, **kwargs):
#         serializer = self.serializer_class(data=request.data, context={"request":request})
#         serializer.is_valid(raise_exception=True)
#         user = serializer.validated_data['user']
#         token, created = Token.objects.get_or_create(user = user)
#         return Response(
#             {
#                 'token':token.key,
#                 'user_id':user.pk,
#                 'email':user.email
#             }
#         )

# --------------------------------------------------------------------------------------------------------

# class CustomDiscardAuthToken(APIView):
#     permission_classes=[IsAuthenticated]

#     def post(self, request):
#         request.user.auth_token.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

# -----------------------------------------------------------------------------------------------------


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerilaizer


# -------------------------------------------------------------------------------------------------------

# class LogoutAPIView(generics.GenericAPIView):
#     serializer_class = LogoutSerializer
#     permission_classes = [IsAuthenticated]

#     def post(self, request):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)

#         token = RefreshToken(serializer.validated_data["refresh"])
#         token.blacklist()


#         return Response(
#             {"detail": "Logout successful"},
#             status=status.HTTP_205_RESET_CONTENT
#         )
# ------------------------------------------------------------------------------------------------------
class ChangePasswordApiView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ChangePassowrdSerializer

    def put(self, request, *args, **kwargs):
        user = request.user
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            if not user.check_password(serializer.validated_data.get("old_password")):
                return Response(
                    {"old_password": "wrong password"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            user.set_password(serializer.validated_data.get("new_password"))
            user.save()
            return Response(
                {"details": "password changed succesfully."},
                status=status.HTTP_200_OK,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ------------------------------------------------------------------------------------------------------------


class ProfileApiView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]
    queryset = Profile.objects.all()

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, user=self.request.user)
        return obj


# ---------------------------------------------------------------------------

# class TestEmailSend(APIView):

#     def get(self, request, *args, **kwargs):
#         self.email = 'ibahare05@gmail.com'
#         user_obj = get_object_or_404(User,email=self.email)
#         token = self.get_tokens_for_users(user_obj)
#         email_obj = EmailMessage('email/hello.tpl', {'token': token}, "admin@admin.com",
#                        to=[self.email])

#         EmailThreading(email_obj).start()
#         return Response({"message": "email sent"})


#     def get_tokens_for_users(self, user):
#         refresh = RefreshToken.for_user(user)
#         return str(refresh.access_token)

# ------------------------------------------------------------------------------------


class ActivationApiView(APIView):
    def get(self, request, token, *args, **kwargs):
        try:
            token = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            user_id = token.get("user_id")

        except ExpiredSignatureError:
            return Response(
                {"detail": "Token has been expired"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        except InvalidSignatureError:
            return Response(
                {"detail": "Token is not valid"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        user_obj = User.objects.get(pk=user_id)
        if user_obj.is_verified:
            return Response({"detail": "your account has been already verified"})
        user_obj.is_verified = True
        user_obj.save()
        return Response({"detail": "your account verified successfilly"})


# ---------------------------------------------------------------------------------------------------------


class ActivationResendApiView(generics.GenericAPIView):
    serializer_class = ActivationResendSerializer

    def post(self, request, *args, **kwargs):
        serializer = ActivationResendSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_obj = serializer.validated_data["user"]
        token = self.get_token_for_users(user_obj)
        email_obj = EmailMessage(
            "email/activation_email.tpl",
            {"token": token},
            "admin@admin.com",
            to=[user_obj.email],
        )
        EmailThreading(email_obj).start()
        return Response({"detail": "User varification resend"})

    def get_token_for_users(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)
