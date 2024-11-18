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
)
from accounts.models import Merchant, Product, Service, Promotion
from accounts.permissions import IsMerchantUser


class CustomPagination(PageNumberPagination):
    page_size = 2
    page_size_query_param = "page_size"
    max_page_size = 50
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
        return Product.objects.filter(merchant__user=self.request.user)

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
        return Service.objects.filter(merchant__user=self.request.user)

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
        return Promotion.objects.filter(product__merchant__user=self.request.user) | Promotion.objects.filter(
            service__merchant__user=self.request.user
        )

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_201_CREATED)
