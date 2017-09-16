#from django.contrib.auth.models import User, Group
from rest_framework import serializers
from app.models import User, Post, Comment

# serializers for returning DB query data to get method

class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    username = serializers.CharField()
    password = serializers.CharField()

class PostSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField()
    category = serializers.CharField()
    timestamp = serializers.DateTimeField(format="'%Y-%m-%d %H:%M:%S'")
    username = serializers.CharField()
    body = serializers.CharField()
    password = serializers.CharField()

class CommentSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    body = serializers.CharField()
    username = serializers.CharField()
    timestamp = serializers.DateTimeField(format="'%Y-%m-%d %H:%M:%S'")
    postId = serializers.IntegerField()
    
    

    