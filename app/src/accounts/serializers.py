from django.core import exceptions
from django.contrib.auth.hashers import check_password
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, Serializer
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from accounts.models import User


class UserCreateSerializer(ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ("email", "password", "first_name", "last_name")

    def validate(self, attrs):
        password = attrs["password"]

        try:
            validate_password(password)
        except exceptions.ValidationError as e:
            raise ValidationError({"password": e})

        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class LogoutSerializer(Serializer):
    refresh = serializers.CharField()

    def validate(self, attrs):
        refresh = attrs["refresh"]

        try:
            RefreshToken(refresh).blacklist()
        except TokenError as e:
            raise ValidationError({"refresh": e})

        return attrs


class UserDetailsSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ("email", "first_name", "last_name", "is_active")
        read_only_fields = ("email",)


class UserDeleteSerializer(Serializer):
    current_password = serializers.CharField(style={"input_type": "password"})

    def validate(self, attrs):
        request = self.context["request"]
        user = request.user
        current_password = attrs["current_password"]

        if check_password(current_password, user.password):
            return attrs
        else:
            raise ValidationError({"current_password": "Invalid password."})
