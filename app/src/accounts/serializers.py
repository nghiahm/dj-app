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


class ProductSerializer(serializers.ModelSerializer):
    merchant = serializers.PrimaryKeyRelatedField(read_only=True)
    category_ids = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), many=True, required=False, write_only=True
    )
    hashtag_ids = serializers.PrimaryKeyRelatedField(
        queryset=Hashtag.objects.all(), many=True, required=False, write_only=True
    )
    keyword_ids = serializers.PrimaryKeyRelatedField(
        queryset=Keyword.objects.all(), many=True, required=False, write_only=True
    )
    categories = CategorySerializer(many=True, read_only=True)
    hashtags = HashtagSerializer(many=True, read_only=True)
    keywords = KeywordSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = "__all__"

    def create(self, validated_data):
        request = self.context["request"]
        merchant = request.user.merchant

        category_ids = validated_data.pop("category_ids", [])
        hashtag_ids = validated_data.pop("hashtag_ids", [])
        keyword_ids = validated_data.pop("keyword_ids", [])

        product = Product.objects.create(merchant=merchant, **validated_data)

        product.categories.set(category_ids)
        product.hashtags.set(hashtag_ids)
        product.keywords.set(keyword_ids)

        return product

    def update(self, instance, validated_data):
        category_ids = validated_data.pop("category_ids", [])
        hashtag_ids = validated_data.pop("hashtag_ids", [])
        keyword_ids = validated_data.pop("keyword_ids", [])

        instance = super().update(instance, validated_data)

        instance.categories.set(category_ids)
        instance.hashtags.set(hashtag_ids)
        instance.keywords.set(keyword_ids)

        return instance


class ServiceSerializer(serializers.ModelSerializer):
    merchant = serializers.PrimaryKeyRelatedField(read_only=True)
    category_ids = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), many=True, required=False, write_only=True
    )
    hashtag_ids = serializers.PrimaryKeyRelatedField(
        queryset=Hashtag.objects.all(), many=True, required=False, write_only=True
    )
    keyword_ids = serializers.PrimaryKeyRelatedField(
        queryset=Keyword.objects.all(), many=True, required=False, write_only=True
    )
    categories = CategorySerializer(many=True, read_only=True)
    hashtags = HashtagSerializer(many=True, read_only=True)
    keywords = KeywordSerializer(many=True, read_only=True)

    class Meta:
        model = Service
        fields = "__all__"

    def create(self, validated_data):
        request = self.context["request"]
        merchant = request.user.merchant

        category_ids = validated_data.pop("category_ids", [])
        hashtag_ids = validated_data.pop("hashtag_ids", [])
        keyword_ids = validated_data.pop("keyword_ids", [])

        service = Service.objects.create(merchant=merchant, **validated_data)

        service.categories.set(category_ids)
        service.hashtags.set(hashtag_ids)
        service.keywords.set(keyword_ids)

        return service

    def update(self, instance, validated_data):
        category_ids = validated_data.pop("category_ids", [])
        hashtag_ids = validated_data.pop("hashtag_ids", [])
        keyword_ids = validated_data.pop("keyword_ids", [])

        instance = super().update(instance, validated_data)

        instance.categories.set(category_ids)
        instance.hashtags.set(hashtag_ids)
        instance.keywords.set(keyword_ids)

        return instance


class PromotionSerializer(serializers.ModelSerializer):
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), source="product", write_only=True, required=False
    )
    service_id = serializers.PrimaryKeyRelatedField(
        queryset=Service.objects.all(), source="service", write_only=True, required=False
    )
    product = ProductSerializer(read_only=True)
    service = ServiceSerializer(read_only=True)
    category_ids = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), many=True, required=False, write_only=True
    )
    hashtag_ids = serializers.PrimaryKeyRelatedField(
        queryset=Hashtag.objects.all(), many=True, required=False, write_only=True
    )
    keyword_ids = serializers.PrimaryKeyRelatedField(
        queryset=Keyword.objects.all(), many=True, required=False, write_only=True
    )
    categories = CategorySerializer(many=True, read_only=True)
    hashtags = HashtagSerializer(many=True, read_only=True)
    keywords = KeywordSerializer(many=True, read_only=True)

    class Meta:
        model = Promotion
        fields = "__all__"

    def validate(self, attrs):
        if not attrs.get("product") and not attrs.get("service"):
            raise ValidationError("A promotion must has a product or a service.")
        return attrs


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
