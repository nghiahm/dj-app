from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView, RetrieveUpdateAPIView, DestroyAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.generics import get_object_or_404
from accounts.serializers import (
    UserCreateSerializer,
    LogoutSerializer,
    UserDetailsSerializer,
    UserDeleteSerializer,
    MerchantSerializer,
)
from accounts.models import Merchant


class UserCreateView(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = UserCreateSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_200_OK)


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
        return Response(status=status.HTTP_200_OK)
