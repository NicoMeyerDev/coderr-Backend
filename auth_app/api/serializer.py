from rest_framework import serializers
from django.contrib.auth.models import User
from auth_app.models import Profile

class RegistrationSerializer(serializers.ModelSerializer):
    repeated_password = serializers.CharField(write_only=True)
    fullname = serializers.CharField(write_only=True)
    type = serializers.ChoiceField(
        choices=Profile.USER_TYPE_CHOICES,
        write_only=True
    )

    class Meta:
        model = User
        fields = ["fullname", "email", "password", "repeated_password", "type"]
        extra_kwargs = {
            "password": {"write_only": True}
        }

    def validate_fullname(self, value):
       
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("This username is already taken.")
        return value

    def validate_email(self, value):
      
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email is already registered.")
        return value

    def validate(self, attrs):
       
        if attrs["password"] != attrs["repeated_password"]:
            raise serializers.ValidationError(
                {"repeated_password": "Passwords do not match."}
            )
        return attrs

    def create(self, validated_data):
        
        validated_data.pop("repeated_password")
        fullname = validated_data.pop("fullname")
        password = validated_data.pop("password")
        type = validated_data.pop("type")

        user = User(
            username=fullname,
            email=validated_data["email"]
        )
        user.set_password(password)
        user.save()
        
        Profile.objects.create(user=user, type=type)
        return user

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
       
        email = data.get("email")
        password = data.get("password")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError(
                {"error": "Email or password is incorrect."}
            )

        if not user.check_password(password):
            raise serializers.ValidationError(
                {"error": "Email or password is incorrect."}
            )

        data["user"] = user
        return data