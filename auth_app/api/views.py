from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken

from .serializers import RegistrationSerializer, LoginSerializer

class RegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        """
        Register a new user, create an auth token, and return
        the relevant account data.
        """
        serializer = RegistrationSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            token, _ = Token.objects.get_or_create(user=user)

            return Response(
                {
                    "token": token.key,
                    "fullname": user.username,
                    "email": user.email,
                    "user_id": user.id
                },
                status=201
            )

        return Response(serializer.errors, status=400)

class CustomLoginView(ObtainAuthToken):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def post(self, request):
        """
        Authenticate a user by email and password and return
        an existing or newly created auth token.
        """
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            user = serializer.validated_data["user"]
            token, _ = Token.objects.get_or_create(user=user)

            return Response(
                {
                    "token": token.key,
                    "fullname": user.username,
                    "email": user.email,
                    "user_id": user.id
                },
                status=200
            )

        return Response(serializer.errors, status=400)

class LogoutView(APIView):

    def post(self, request):
        """
        Delete the current user's auth token to log the user out.
        """
        request.user.auth_token.delete()
        return Response(
            {"detail": "Logout successful. Token was deleted."},
            status=status.HTTP_200_OK
        )