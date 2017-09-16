from django.conf.urls import url, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browseable API.
urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^blog/postlist', views.PostList, name='PostList'),
    url(r'^blog/post/(\d+)/commentlist', views.CommentList, name='CommentList'),
    url(r'^blog/register', views.Register, name='Register'),
    url(r'^blog/post', views.WritePost, name='WritePost'),
    url(r'^blog/comment', views.WriteComment, name='WriteComment'),
    url(r'^blog/login', views.Login, name='Login'),

    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]