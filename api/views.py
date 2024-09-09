from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']
        extra_kwargs = {
            'username': {'required': True},
            'password': {'write_only': True}
        }



# from django.shortcuts import render
# from rest_framework import status
# from rest_framework import viewsets
# from rest_framework.response import Response
# from rest_framework import generics
# from rest_framework.exceptions import NotFound
# from rest_framework.views import APIView
# from rest_framework.permissions import AllowAny
# from registration.models import CustomUser
# from .serializers import CustomUserSerializer

# class UserListCreateView(generics.ListCreateAPIView):
#     queryset = CustomUser.objects.all()
#     serializer_class = CustomUserSerializer
#     permission_classes = [AllowAny]

#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)

#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)

# class UserDetailView(generics.RetrieveUpdateAPIView):
#     queryset = CustomUser.objects.all()
#     serializer_class = CustomUserSerializer
#     permission_classes = [AllowAny]

#     def get(self, request, *args, **kwargs):
#         try:
#             instance = self.get_object()
#         except CustomUser.DoesNotExist:
#             return Response(status=status.HTTP_404_NOT_FOUND)

#         if request.method == 'GET':
#             return self.retrieve(request, *args, **kwargs)
#         elif request.method == 'PUT':
#             return self.partial_update(request, *args, **kwargs)
#         else:
#             raise NotFound()

# class RegisterUserView(APIView):
#     permission_classes = [AllowAny]

#     def post(self, request):
#         serializer = CustomUserSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class UserViewSet(viewsets.ViewSet):
#     def list(self, request):
#         queryset = CustomUser.objects.all()
#         serializer = CustomUserSerializer(queryset, many=True)
#         return Response(serializer.data)

#     def create(self, request):
#         serializer = CustomUserSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def retrieve(self, request, pk=None):
#         try:
#             instance = CustomUser.objects.get(pk=pk)
#         except CustomUser.DoesNotExist:
#             return Response(status=status.HTTP_404_NOT_FOUND)

#         serializer = CustomUserSerializer(instance)
#         return Response(serializer.data)

#     def partial_update(self, request, pk=None):
#         try:
#             instance = CustomUser.objects.get(pk=pk)
#         except CustomUser.DoesNotExist:
#             return Response(status=status.HTTP_404_NOT_FOUND)

#         serializer = CustomUserSerializer(instance, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)