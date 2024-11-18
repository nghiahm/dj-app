from django.core import exceptions
from django.db import IntegrityError
from django.contrib.auth.hashers import check_password
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, Serializer
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from accounts.models import User, Merchant, Product, Service, Promotion, Category, Hashtag, Keyword


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


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "email", "first_name", "last_name", "is_active")


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class HashtagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hashtag
        fields = "__all__"


class KeywordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Keyword
        fields = "__all__"


class PromotionSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True, read_only=True)
    hashtags = HashtagSerializer(many=True, read_only=True)
    keywords = KeywordSerializer(many=True, read_only=True)

    class Meta:
        model = Promotion
        fields = "__all__"

    def validate(self, attrs):
        if not attrs.get("product") and not attrs.get("service"):
            raise ValidationError("A promotion must be associated with either a product or a service.")
        return attrs


class ProductSerializer(serializers.ModelSerializer):
    merchant = serializers.PrimaryKeyRelatedField(read_only=True)
    categories = CategorySerializer(many=True, read_only=True)
    hashtags = HashtagSerializer(many=True, read_only=True)
    keywords = KeywordSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = "__all__"

    def create(self, validated_data):
        request = self.context["request"]
        merchant = request.user.merchant
        product = Product.objects.create(merchant=merchant, **validated_data)
        return product


class ServiceSerializer(serializers.ModelSerializer):
    merchant = serializers.PrimaryKeyRelatedField(read_only=True)
    categories = CategorySerializer(many=True, read_only=True)
    hashtags = HashtagSerializer(many=True, read_only=True)
    keywords = KeywordSerializer(many=True, read_only=True)

    class Meta:
        model = Service
        fields = "__all__"

    def create(self, validated_data):
        request = self.context["request"]
        merchant = request.user.merchant
        service = Service.objects.create(merchant=merchant, **validated_data)
        return service


class MerchantSerializer(ModelSerializer):
    user = UserSerializer(read_only=True)
    products = ProductSerializer(many=True, read_only=True)
    services = ServiceSerializer(many=True, read_only=True)

    class Meta:
        model = Merchant
        fields = "__all__"

    def create(self, validated_data):
        request = self.context["request"]
        user = request.user
        try:
            merchant = Merchant.objects.create(user=user, **validated_data)
        except IntegrityError:
            raise ValidationError("You can only create one merchant per user.")
        return merchant
