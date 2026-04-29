from rest_framework import serializers
from django.contrib.auth.models import User
from auth_app.models import Profile

class RegistrationSerializer(serializers.ModelSerializer):
    repeated_password = serializers.CharField(write_only=True)
    username = serializers.CharField(write_only=True)
    type = serializers.ChoiceField(
        choices=Profile.USER_TYPE_CHOICES,
        write_only=True
    )

    class Meta:
        model = User
        fields = ["username", "email", "password", "repeated_password", "type"] #
        extra_kwargs = {
            "password": {"write_only": True}
        }

    def validate_username(self, value):
       
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
        username = validated_data.pop("username")
        password = validated_data.pop("password")
        type = validated_data.pop("type")

        user = User(
            username=username,
            email=validated_data["email"]
        )
        user.set_password(password)
        user.save()
        
        Profile.objects.create(user=user, type=type)
        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
       
        username = data.get("username")
        password = data.get("password")

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise serializers.ValidationError(
                {"error": "Username or password is incorrect."}
            )

        if not user.check_password(password):
            raise serializers.ValidationError(
                {"error": "Username or password is incorrect."}
            )

        data["user"] = user
        return data
    
class ProfileSerializer(serializers.ModelSerializer):
        user = serializers.IntegerField(source="user.id", read_only=True)
        username = serializers.CharField(source="user.username", read_only=True)
        first_name = serializers.CharField(source="user.first_name", read_only=True)
        last_name = serializers.CharField(source="user.last_name", read_only=True)
        email = serializers.EmailField(source="user.email", read_only=True)

        class Meta:
            model = Profile
            fields = ["user", "username", "first_name", "last_name", "file", "location", "tel", "description", "working_hours", "type", "email", "created_at"]   

class ProfileUpdateSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source="user.first_name", required=False, allow_blank=True)
    last_name = serializers.CharField(source="user.last_name", required=False, allow_blank=True)
    email = serializers.EmailField(source="user.email", required=False)
    location = serializers.CharField(required=False, allow_blank=True)
    tel = serializers.CharField(required=False, allow_blank=True)
    description = serializers.CharField(required=False, allow_blank=True)
    working_hours = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = Profile
        fields = [
            "first_name",
            "last_name",
            "email",
            "location",
            "tel",
            "description",
            "working_hours",
            
        ]

    def update(self, instance, validated_data):
        user_data = validated_data.pop("user", {})

        user = instance.user
        user.first_name = user_data.get("first_name", user.first_name)
        user.last_name = user_data.get("last_name", user.last_name)
        user.email = user_data.get("email", user.email)
        user.save()

        instance.location = validated_data.get("location", instance.location)
        instance.tel = validated_data.get("tel", instance.tel)
        instance.description = validated_data.get("description", instance.description)
        instance.working_hours = validated_data.get("working_hours", instance.working_hours)
        instance.save()

        return instance  

class BusinessProfileSerializer(ProfileSerializer):
    class Meta(ProfileSerializer.Meta):
            model = Profile
            fields = ["user", "username", "first_name", "last_name", "file", "location", "tel", "description", "working_hours","type"]

class CustomerProfileSerializer(ProfileSerializer):
    uploaded_at = serializers.DateTimeField(source="created_at", read_only=True)
    class Meta(ProfileSerializer.Meta):
            model = Profile
            fields = ["user", "username", "first_name", "last_name", "file", "uploaded_at", "type"]                      