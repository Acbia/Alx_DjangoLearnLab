from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_user, name='register'),
    path('login/', views.user_login, name='login'),
    path('profile/', views.user_profile, name='profile'),
    path('follow/<int:user_id>/', views.FollowUserView.as_view(), name='follow'),
    path('unfollow/<int:user_id>/', views.UnfollowUserView.as_view(), name='unfollow'),
    path('following/', views.FollowingListView.as_view(), name='following-list'),
    path('followers/', views.FollowersListView.as_view(), name='followers-list'),
    path('user/<int:user_id>/', views.UserProfileDetailView.as_view(), name='user-profile-detail'),
]