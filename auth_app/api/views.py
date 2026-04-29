from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.exceptions import NotFound
from rest_framework.generics import ListAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from auth_app.api.permissions import IsProfileOwnerOrReadOnly
from auth_app.models import Profile

from .serializer import BusinessProfileSerializer, CustomerProfileSerializer, RegistrationSerializer, LoginSerializer, ProfileSerializer, ProfileUpdateSerializer

class RegistrationView(APIView):
    """Handles user registration and token creation."""
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
                    "username": user.username,
                    "email": user.email,
                    "user_id": user.id
                },
                status=201
            )

        return Response(serializer.errors, status=400)

class CustomLoginView(ObtainAuthToken):
    """Handles user authentication and token retrieval."""
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
                    "username": user.username,
                    "email": user.email,
                    "user_id": user.id
                },
                status=200
            )

        return Response(serializer.errors, status=400)

class ProfileView(RetrieveUpdateAPIView):
    """Retrieves and updates user profiles."""
    permission_classes = [IsAuthenticated, IsProfileOwnerOrReadOnly]

    def get_object(self):
        try:
            profile = Profile.objects.get(user__id=self.kwargs["pk"])
        except Profile.DoesNotExist:
            raise NotFound({"detail": "Profil nicht gefunden."})
        self.check_object_permissions(self.request, profile)
        return profile
    
    
    def get_serializer_class(self):
        if self.request.method == "PATCH":
            return ProfileUpdateSerializer
        return ProfileSerializer
    
    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        write_serializer = ProfileUpdateSerializer(instance=instance, data=request.data, partial=True)
        write_serializer.is_valid(raise_exception=True)
        write_serializer.save()
        read_serializer = ProfileSerializer(instance)   
        return Response(read_serializer.data, status=status.HTTP_200_OK)
    


class BusinessProfileListView(ListAPIView):
    """Lists all business profiles."""
    serializer_class = BusinessProfileSerializer
    pagination_class = None

    def get_queryset(self):
        return Profile.objects.filter(type="business")

class CustomerProfileListView(ListAPIView):
    """Lists all customer profiles."""
    serializer_class = CustomerProfileSerializer
    pagination_class = None

    def get_queryset(self):
        return Profile.objects.filter(type="customer")        