from .models import User
from rest_framework import serializers
from django.contrib.auth import authenticate


class SignupSerailizer(serializers.Serializer):
    email = serializers.EmailField()
    name = serializers.CharField()
    password = serializers.CharField()
    confirmpassword = serializers.CharField()
    
    def validate(self, attrs):
        
        if attrs['password'] != attrs['confirmpassword']:
            raise serializers.ValidationError({"message":"password mismatched"})
        
        return super().validate(attrs)


class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = '__all__'

class SignInSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    user_details = serializers.SerializerMethodField()

    def validate(self, attrs):
        email = attrs.get('email', '').lower()
        password = attrs.get('password', '')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError({'message': "User does not exist"})

        user = authenticate(email=email, password=password)

        if not user:
            raise serializers.ValidationError({'message': "Invalid credentials"})

        if not user.is_active:
            raise serializers.ValidationError({'message': "User is deactivated"})

        self.user = user  # Store the user instance
        return attrs

    def get_user_details(self, obj):
        user = getattr(self, 'user', None)
        if user:
            return {
                'user_id': user.id,
                'name': getattr(user, 'display_name', user.username),
                'email': user.email
            }
        return {}