from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserSerializer

User = get_user_model()

class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)







# from rest_framework import serializers
# from registration.models import CustomUser
# import re
# from otp_project import settings



# class CustomUserSerializer(serializers.ModelSerializer):
#     password = serializers.CharField(write_only=True)
#     class Meta:
#         model = CustomUser
#         fields = ['id', 'first_name', 'last_name', 'email', 'phone_number', 'role', 'is_active', 'is_staff', 'password']
#         read_only_fields = ['id', 'is_active', 'is_staff']
#     def validate_password(self, value):
#         if not (8 <= len(value) <= 16 and re.search(r'\d', value) and re.search(r'[!@#$%^&*(),.?":{}|<>]', value)):
#             raise serializers.ValidationError('Password must be between 8 and 16 characters and include special characters and numbers.')
#         return value
#     def validate_phone_number(self, value):
#         if not re.match(r'^\d{10,13}$', value):
#             raise serializers.ValidationError('Phone number must be between 10 and 13 digits.')
#         return value
#     def create(self, validated_data):
#         password = validated_data.pop('password')
#         user = CustomUser(**validated_data)
#         user.set_password(password)
#         user.save()
#         return user
#     def update(self, instance, validated_data):
#         for attr, value in validated_data.items():
#             if attr == 'password':
#                 instance.set_password(value)
#             else:
#                 setattr(instance, attr, value)
#         instance.save()
#         return instance









