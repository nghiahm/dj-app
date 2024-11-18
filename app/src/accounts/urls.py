from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.routers import DefaultRouter
from accounts.views import (
    UserCreateView,
    LogoutView,
    UserDetailsView,
    UserDeleteView,
    MerchantViewSet,
    ProductViewSet,
    ServiceViewSet,
    PromotionViewSet,
)


router = DefaultRouter()
router.register("products", ProductViewSet, basename="products")
router.register("services", ServiceViewSet, basename="services")
router.register("promotions", PromotionViewSet, basename="promotions")

urlpatterns = [
    path("signup/", UserCreateView.as_view(), name="signup"),
    path("token/", TokenObtainPairView.as_view(), name="login"),
    path("token/refresh/", TokenRefreshView.as_view(), name="refresh-token"),
    path("token/blacklist/", LogoutView.as_view(), name="logout"),
    path("details/", UserDetailsView.as_view(), name="user-details"),
    path("delete/", UserDeleteView.as_view(), name="delete-user"),
    path(
        "merchants/",
        MerchantViewSet.as_view(
            {"post": "create", "get": "retrieve", "put": "partial_update", "patch": "update", "delete": "destroy"}
        ),
        name="merchant-api",
    ),
] + router.urls
