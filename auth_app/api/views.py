from rest_framework.generics import RetrieveUpdateAPIView, ListAPIView
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from auth_app.models import Profile
from .serializer import RegistrationSerializer, LoginSerializer, ProfileSerializer, ProfileUpdateSerializer

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

class ProfileView(RetrieveUpdateAPIView):
    queryset = Profile.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == "PATCH":
            return ProfileUpdateSerializer
        return ProfileSerializer

    def get_queryset(self):
        return Profile.objects.filter(user=self.request.user)
    
class BusinessProfileListView(ListAPIView):
    serializer_class = ProfileSerializer

    def get_queryset(self):
        return Profile.objects.filter(type="business")

class CustomerProfileListView(ListAPIView):
    serializer_class = ProfileSerializer

    def get_queryset(self):
        return Profile.objects.filter(type="customer")        