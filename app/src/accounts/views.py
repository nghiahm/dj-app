from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView, RetrieveUpdateAPIView, DestroyAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from accounts.serializers import (
    UserCreateSerializer,
    LogoutSerializer,
    UserDetailsSerializer,
    UserDeleteSerializer,
    MerchantSerializer,
    ProductSerializer,
    ServiceSerializer,
    PromotionSerializer,
    CategorySerializer,
)
from accounts.models import Merchant, Product, Service, Promotion, Category, Hashtag, Keyword
from accounts.permissions import IsMerchantUser


class CustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100
    page_query_param = "p"


class UserCreateView(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = UserCreateSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_201_CREATED)


class LogoutView(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = LogoutSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(status=status.HTTP_200_OK)


class UserDetailsView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserDetailsSerializer

    def get_object(self):
        return self.request.user


class UserDeleteView(DestroyAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserDeleteSerializer

    def delete(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = request.user
        self.perform_destroy(user)
        return Response(status=status.HTTP_200_OK)


class MerchantViewSet(ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = MerchantSerializer

    def get_queryset(self):
        return Merchant.objects.filter(user=self.request.user)

    def get_object(self):
        self.queryset = self.get_queryset()
        obj = get_object_or_404(self.queryset, user=self.request.user)
        return obj

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_201_CREATED)


class ProductViewSet(ModelViewSet):
    permission_classes = (IsAuthenticated, IsMerchantUser)
    serializer_class = ProductSerializer
    lookup_field = "pk"
    pagination_class = CustomPagination

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return Product.objects.none()
        return Product.objects.filter(merchant__user=self.request.user).order_by("pk")

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_201_CREATED)


class ServiceViewSet(ModelViewSet):
    permission_classes = (IsAuthenticated, IsMerchantUser)
    serializer_class = ServiceSerializer
    lookup_field = "pk"
    pagination_class = CustomPagination

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return Service.objects.none()
        return Service.objects.filter(merchant__user=self.request.user).order_by("pk")

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_201_CREATED)


class PromotionViewSet(ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = PromotionSerializer
    lookup_field = "pk"
    pagination_class = CustomPagination

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return Promotion.objects.none()
        return Promotion.objects.filter(product__merchant__user=self.request.user).order_by(
            "pk"
        ) | Promotion.objects.filter(service__merchant__user=self.request.user).order_by("pk")

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_201_CREATED)


class CategoryViewSet(ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = CategorySerializer
    pagination_class = CustomPagination
    queryset = Category.objects.all().order_by("pk")
    lookup_field = "pk"


class HashtagViewSet(ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = CategorySerializer
    pagination_class = CustomPagination
    queryset = Hashtag.objects.all().order_by("pk")
    lookup_field = "pk"


class KeywordViewSet(ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = CategorySerializer
    pagination_class = CustomPagination
    queryset = Keyword.objects.all().order_by("pk")
    lookup_field = "pk"
