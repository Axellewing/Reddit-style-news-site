from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("signup", views.signup, name="signup"),
    path("likes", views.likes, name="likes"),
    path("search", views.search, name="search"),
    path("signin", views.signin, name="signin"),
    path("logout", views.logout, name="logout"),
    path("settings", views.settings, name="settings"),
    path("upload", views.upload, name="upload"),
    path("follow", views.follow, name="follow"),
    path("profile/<str:username>", views.profile, name="profile"),
    path('delete_profile', views.delete_profile, name='delete_profile'),
    path('post/<uuid:id_post>', views.post, name='post'),
    path('delete_post/<uuid:id_post>', views.delete_post, name='delete_post'),
    path('<path:path>', views.handler404),
]