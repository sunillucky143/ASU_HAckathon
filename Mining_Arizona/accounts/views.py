from rest_framework.decorators import api_view
from .serializer import RegistrationSerializer
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model

@api_view(['POST'])
def register(request):
    if request.method == 'POST':
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# In your views.py

class LoginView(APIView):
        def post(self, request):
            username = request.data.get('username')
            print(username)
            password = request.data.get('password')
            print(password)

            if not username or not password:
                return Response({'error': 'Username and password are required'}, status=status.HTTP_400_BAD_REQUEST)

            # Check if it's an email login
            if '@' in username:
                User = get_user_model()
                try:
                    email_user = User.objects.get(email=username)
                except User.DoesNotExist:
                    return Response({'error': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)

                # Authenticate manually by checking the password
                if email_user.check_password(password):
                    token, created = Token.objects.get_or_create(user=email_user)
                    return Response({'token': token.key}, status=status.HTTP_200_OK)
                else:
                    return Response({'error': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)

            # Username-based authentication
            user = authenticate(request, username=username, password=password)
            if user is not None:
                token, created = Token.objects.get_or_create(user=user)
                return Response({'token': token.key}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)