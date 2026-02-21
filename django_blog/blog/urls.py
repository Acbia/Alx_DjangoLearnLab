from django.urls import path
from . import views
from .views import (
     PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    CommentCreateView,
    CommentUpdateView,
    CommentDeleteView,
    add_comment,
    edit_comment,
    delete_comment, 
     SearchResultsView, 
     TagPostListView,
     PostByTagListView,
)

urlpatterns = [
    path("register/", views.register_view, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("profile/", views.profile_view, name="profile"),

    path('', PostListView.as_view(), name='post_list'),
    path('post/new/', PostCreateView.as_view(), name='post_create'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post_update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),

    path('post/<int:pk>/comments/new/', views.add_comment, name='add_comment'),
    path("comment/<int:pk>/update/", CommentUpdateView.as_view(), name="comment-update"),
    path("comment/<int:pk>/delete/", CommentDeleteView.as_view(), name="comment-delete"),
     path('tags/<slug:tag_slug>/', PostByTagListView.as_view(), name='posts-by-tag'),

    path("search/", SearchResultsView.as_view(), name="search"),
    path("tags/<str:tag_name>/", TagPostListView.as_view(), name="tag-posts"),
]
