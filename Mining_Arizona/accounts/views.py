from rest_framework.decorators import api_view
from django.http import JsonResponse
from rest_framework_simplejwt.tokens import RefreshToken
from .serializer import *
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from accounts.models import *

@api_view(['POST'])
def register(request):
    if request.method == 'POST':
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# In your views.py
def comment_count(request):
        try:
            count = Comments.objects.count()
            print(count)
            return JsonResponse({'count': count})
        except Exception as e:
            print(f"Error occurred: {e}")
            return JsonResponse({'error': 'An error occurred while fetching the comment count.'}, status=500)


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
                    refresh = RefreshToken.for_user(email_user)
                    return Response({
                        'refresh': str(refresh),
                        'access': str(refresh.token),
                    }, status=status.HTTP_200_OK)
                else:
                    return Response({'error': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)

            # Username-based authentication
            user = authenticate(request, username=username, password=password)
            if user is not None:
                refresh = RefreshToken.for_user(user)
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.token),
                }, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class PostView(APIView):
    def get(self, request):
        output = [{'post_id':output.unique_id,
                   'procedure': output.procedure,
                   'saftey_protocols': output.s_p,
                   'lawsAndRegulations': output.l_a_r}
                  for output in Post.objects.all()]
        return Response(output)
    def post(self, request):
        post_serializer = PostSerializer(data=request.data)
        if post_serializer.is_valid(raise_exception=True):
            post_serializer.save()
            return Response(post_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(post_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# views.py

class CommentView(APIView):
    def get(self, request):
        output = [{'post_id': comment.post_id, 'comment': comment.comment, 'risk_factor': comment.risk_factor} for comment in Comments.objects.all()]

        if output:
            return Response(output, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'No comments found for this post.'}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        # Attach post_id to the request data
        comment_serializer = CommentSerializer(data=request.data)

        if comment_serializer.is_valid(raise_exception=True):
            comment_serializer.save()
            return Response(comment_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(comment_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

