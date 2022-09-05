
from django.urls import path
from .views import likepost, postview,unlikepost,AddComment,AddReply,subscribe,home,searchPost
urlpatterns = [
    path('<int:id>', postview,name='post'),
    path('like/<int:id>',likepost,name='likepost'),
    path('unlike/<int:id>',unlikepost,name='unlikepost'),
    path('subscribe/<int:id>',subscribe,name='subscribe'),
    path('addcomment/<int:id>',AddComment.as_view(),name='addcomment'),
    path('addreply/<int:id>',AddReply.as_view(),name='addreply'),
    path('home', home, name='homepage'),
    path('search/',searchPost, name="search"),
]
