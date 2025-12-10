from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    path("signup/", views.signup_view, name="signup"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("settings/", views.account_settings, name="settings"),
    path("profile/<str:username>/", views.user_profile, name="user_profile"),
    path("follow/<str:username>/", views.follow_toggle, name="follow_toggle"),
    path("search/", views.user_search, name="user_search"),
]
