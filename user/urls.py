from django.urls import path,include
from . import views

# import notifications.urls

from .views import MyTokenObtainPairView
from rest_framework import routers
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('',views.getRoutes),
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('signup/',views.userSignup),
    path('proposal',views.proposal),
    path('proposals/<id>',views.post),
    path('mentors',views.register_mentor),
    path('mentor_list',views.mentor_list),
    path('approve_user/<id>',views.request_verify),
    
    path('profileImage/<id>',views.profileImage),
    path('changeprofileImage/<id>',views.change_profile),
    path('requesttoverify',views.request_to_verify),
      path('userlist',views.userList),
      path('allusers',views.all_users),
      path('users',views.users),
        path('userCheck/<id>',views.userCheck),
      path('userDetailview/<id>',views.usersDetailView),
       path('postcreate',views.postCreate),
    path('google_signin',views.google_signin),
    path('post',views.posts),
    path('follow_check/<id>',views.follow_user),
    path('follow/<id>',views.follow_get),
     path('unfollow/<id>/<uid>',views.unfollow),
    path('postget/<id>',views.postget),
    path('followget/<id>',views.follow_get),
    path('followgets/<id>',views.follow_gets),
    path('followers/<id>',views.followers_get),
    path('like/<id>/<uid>',views.like),
    path('like_show/<id>/<uid>',views.like),
    path('dislike/<id>/<uid>',views.like),
    path('countLike/<id>',views.like_count),
    path('notify',views.notify),
    path('saved/',views.saved),
    path('saved/<id>',views.savedget),
    path('saved/<pid>/<id>',views.check_saved),
    path('rooms',views.create_room),
    path('rooms/<sender>/<receiver>',views.get_room),
    path('chatmessages/<id>',views.messages),
    path('notify_get/<id>',views.notify_get),
    # path('inbox/notifications/', include(notifications.urls, namespace='notifications')),

   
]
