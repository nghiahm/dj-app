from django.core import exceptions
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from rest_framework.exceptions import ValidationError
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
