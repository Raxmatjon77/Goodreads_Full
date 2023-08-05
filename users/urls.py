# from django.urls import path

# from users.views import RegisterView,LoginView,ProfileView,LogoutView,ProfileUpdate

# urlpatterns=[
#     path('register/',RegisterView.as_view(),name='register'),
#     path('login/',LoginView.as_view(), name='login'),
#     path('logout/',LogoutView.as_view(), name='logout'),

#     path('profile/',ProfileView.as_view(),name='profile'),
#     path('profile/update',ProfileUpdate.as_view(),name='profile_update')
# ]
from django.urls import path
from users.views import RegisterView, LoginView, ProfileView, LogoutView, ProfileUpdate, SendFriendRequestView, AcceptFriendRequestView, RejectFriendRequestView, UnfriendView,\
    GetInTouchView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/',ProfileView.as_view(), name='profile'),
    path('profile/update', ProfileUpdate.as_view(), name='profile_update'),
    path('profile/friend-request/<int:receiver_id>/', SendFriendRequestView.as_view(), name='send_friend_request'),
    path('profile/friend-request/accept/<int:friendship_id>/', AcceptFriendRequestView.as_view(), name='accept_friend_request'),
    path('profile/friend-request/reject/<int:friendship_id>/', RejectFriendRequestView.as_view(), name='reject_friend_request'),
    path('profile/unfriend/<int:friend_id>/', UnfriendView.as_view(), name='unfriend'),
 
]
