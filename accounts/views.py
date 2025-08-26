from django.shortcuts import render
from rest_framework import status, generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .serializers import (UserSerializer, UserProfileSerializer, RegisterSerializer,
                         LoginSerializer, ChangePasswordSerializer)
from .models import UserProfile

# Create your views here.

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegisterSerializer

class LoginView(generics.GenericAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = LoginSerializer
    
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = authenticate(
            username=serializer.validated_data['username'],
            password=serializer.validated_data['password']
        )
        
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'user': UserSerializer(user).data
            })
        else:
            return Response({
                'error': 'Invalid credentials'
            }, status=status.HTTP_401_UNAUTHORIZED)

class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = (permissions.IsAuthenticated,)
    
    def get_object(self):
        return self.request.user.profile

class ChangePasswordView(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = (permissions.IsAuthenticated,)
    
    def update(self, request, *args, **kwargs):
        user = request.user
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        if not user.check_password(serializer.data.get('old_password')):
            return Response({'error': 'Wrong password'}, status=status.HTTP_400_BAD_REQUEST)
        
        user.set_password(serializer.data.get('new_password'))
        user.save()
        return Response({'message': 'Password updated successfully'})

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def logout(request):
    try:
        request.user.auth_token.delete()
        return Response({'message': 'Successfully logged out'})
    except:
        return Response({'error': 'Error logging out'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def user_info(request):
    return Response({
        'user': UserSerializer(request.user).data,
        'profile': UserProfileSerializer(request.user.profile).data
    })
