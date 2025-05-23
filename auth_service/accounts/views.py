from rest_framework import generics, status
from rest_framework.response import Response
from .models import User
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate

class RegisterView(generics.CreateAPIView):
    def post(self, request):
        email = request.data.get('email')
        phone = request.data.get('phone')
        password = request.data.get('password')

        if User.objects.filter(email=email).exists():
            return Response({'error': 'Email already registered'}, status=400)

        user = User.objects.create_user(email=email, phone=phone, password=password)
        return Response({'message': 'User registered'}, status=201)

class LoginView(generics.GenericAPIView):
    def post(self, request):
        email = request.data.get('email')
        phone = request.data.get('phone')
        password = request.data.get('password')

        # You can authenticate with either
        user = None
        if email:
            user = authenticate(request, email=email, password=password)
        elif phone:
            try:
                user_obj = User.objects.get(phone=phone)
                user = authenticate(request, email=user_obj.email, password=password)
            except User.DoesNotExist:
                pass

        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        return Response({'error': 'Invalid credentials'}, status=401)
