from django.shortcuts import render

from app.models import User, Post, Comment
from rest_framework import viewsets
from app.serializers import UserSerializer, PostSerializer, CommentSerializer

from rest_framework.renderers import JSONRenderer
from rest_framework.decorators import api_view, renderer_classes, authentication_classes
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from django.db.models import F

from rest_framework_jwt.settings import api_settings
from django.contrib.auth import get_user_model


import json

from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from rest_framework.authentication import (
    BaseAuthentication, get_authorization_header
)



# return the post list
@api_view(['GET'])
def PostList(request):
    if request.method == 'GET':
        #posts = Post.objects.select_related().annotate(username=F('user__username')).annotate(password=F('user__password')).order_by('-timestamp')
        posts = Post.objects.select_related().extra(select={'username':'app_user.username', 'password': 'app_user.password'}).order_by('-timestamp')
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

# return the comment list of a specifc post
@api_view(['GET'])
def CommentList(request, postId):
    if request.method == 'GET':
        comments = Comment.objects.select_related().filter(post__id = postId).extra(select={'username':'app_user.username', 'postId': 'app_post.id'}).order_by('-timestamp')
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)


# register a new user
@api_view(['POST'])
@renderer_classes((JSONRenderer,))
def Register(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))

        username = data["username"]
        password = data["password"]

        user = User.objects.filter(username = username).all()
       
        if len(user) != 0:
             return Response({
            'status': 'failure',
            'msg': 'username taken!'
            }) 
        else:
            User.objects.create(username = username, password=password)
            return Response({
            'status': 'success',
            'msg': 'succeed!'
            })


# submit a new post
@api_view(['POST'])
@authentication_classes((JSONWebTokenAuthentication,))
@renderer_classes((JSONRenderer,))
def WritePost(request):
    if request.method == 'POST':

        data = json.loads(request.body.decode('utf-8'))

        title = data["title"]
        category = data["category"]
        body = data["body"]

        Post.objects.create(title = title, body=body, category=category, user = request.user)

        return Response({
        'status': 'success',
        'msg': 'succeed!'
        })


# submit a comment of a specific post
@api_view(['POST'])
@authentication_classes((JSONWebTokenAuthentication,))
@renderer_classes((JSONRenderer,))
def WriteComment(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))

        postId = data["postId"]
        comment = data["comment"]

        Comment.objects.create(body = comment
            ,user = request.user
            ,post_id = int(postId))

        return Response({
        'status': 'success',
        'msg': 'succeed!'
        })

# login entry, mannually creating the jwt token as we want to have the separated login entry
@api_view(['POST'])
@renderer_classes((JSONRenderer,))
def Login(request):
    if request.method == 'POST':

        data = json.loads(request.body.decode('utf-8'))

        username = data["username"]
        password = data["password"]

        user = User.objects.filter(username = username, password=password).all()
        print(len(user))
        
        if len(user) != 1:
            return Response({
                "description": "Invalid credentials",
                "error": "Bad Request",
                "status_code": 401
            }) 
        else:
            jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
            jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

            payload = jwt_payload_handler(user[0])
            print(payload)
            token = jwt_encode_handler(payload)
            return Response({
            'access_token': token,
            })