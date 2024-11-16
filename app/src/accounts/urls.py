from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from accounts.views import UserCreateView, LogoutView, UserDetailsView, UserDeleteView

urlpatterns = [
    path("signup/", UserCreateView.as_view(), name="signup"),
    path("token/", TokenObtainPairView.as_view(), name="login"),
    path("token/refresh/", TokenRefreshView.as_view(), name="refresh-token"),
    path("token/blacklist/", LogoutView.as_view(), name="logout"),
    path("details/", UserDetailsView.as_view(), name="user-details"),
    path("delete/", UserDeleteView.as_view(), name="delete-user"),
]
