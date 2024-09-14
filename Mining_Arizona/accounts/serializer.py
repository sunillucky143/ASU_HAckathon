from tokenize import Comment

from rest_framework import serializers
from django.contrib.auth.models import User

from accounts.models import Post


class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'password')  # Adjust fields according to your User model or custom model
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model=Post
        fields = ['procedure', 's_p', 'l_a_r', 'access']

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model=Comment
        fields = '__all__'