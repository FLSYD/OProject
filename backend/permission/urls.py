from django.urls import path

from .views import AvatarView, ChangePasswordView, ExampleView, HealthView, LoginView, MenuView, ProfileView

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("menu/", MenuView.as_view(), name="menu"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("profile/password/", ChangePasswordView.as_view(), name="change-password"),
    path("profile/avatar/", AvatarView.as_view(), name="avatar"),
    path("example/", ExampleView.as_view(), name="example"),
    path("health/", HealthView.as_view(), name="health"),
]

