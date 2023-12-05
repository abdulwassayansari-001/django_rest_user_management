from rest_framework import serializers
from users.models import User, Child

class RegisterSerializer(serializers.ModelSerializer):

    password = serializers.CharField(max_length=128, min_length = 6, write_only=True)

    class Meta:
        model = User
        fields = ('username','email', 'password')

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
    

class LoginSerializer(serializers.ModelSerializer):

    password = serializers.CharField(max_length=128, min_length = 6, write_only=True)

    class Meta:
        model = User
        fields = ('email', 'password', 'token')

        read_only_field = ['token']



from django.contrib.auth import get_user_model

class ChildSerializer(serializers.ModelSerializer):
    class Meta:
        model = Child
        fields = ('username', 'email', 'password')  # Include the necessary fields for child registration

    def create(self, validated_data):
        # Get the parent from the request context (assumes the request is available in the serializer context)
        parent = self.context['request'].user

        # Extract child-specific data from validated_data
        username = validated_data.pop('username', None)
        email = validated_data.pop('email', None)
        password = validated_data.pop('password', None)

        # Check if 'username', 'email', and 'password' are present
        if username is None or email is None or password is None:
            raise serializers.ValidationError({'detail': 'Username, email, and password are required fields.'})

        # Create User instance for the child
        user = get_user_model().objects.create_user(username=username, email=email, password=password)
        
        # Create Child instance with parent and child-specific data
        child = Child.objects.create(parent=parent, username=username, email=email, password=password, **validated_data)
        return child

