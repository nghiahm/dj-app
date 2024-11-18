from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from accounts.managers import UserManager


class User(AbstractUser):
    username = None
    email = models.EmailField(_("email address"), unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    objects = UserManager()

    class Meta:
        ordering = ["-date_joined"]

    def __str__(self):
        return self.email


class Merchant(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"{self.user} - merchant"


class Category(models.Model):
    name = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.name


class Hashtag(models.Model):
    name = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.name


class Keyword(models.Model):
    name = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    merchant = models.ForeignKey(Merchant, on_delete=models.CASCADE, related_name="products")
    name = models.CharField(max_length=255, blank=True)
    categories = models.ManyToManyField(Category, related_name="products", blank=True)
    hashtags = models.ManyToManyField(Hashtag, related_name="products", blank=True)
    keywords = models.ManyToManyField(Keyword, related_name="products", blank=True)

    def __str__(self):
        return self.name

    def get_categories(self):
        return "\n".join([p.categories for p in self.categories.all()])

    def get_hashtags(self):
        return "\n".join([p.hashtags for p in self.hashtags.all()])

    def get_keywords(self):
        return "\n".join([p.keywords for p in self.keywords.all()])


class Service(models.Model):
    merchant = models.ForeignKey(Merchant, on_delete=models.CASCADE, related_name="services")
    name = models.CharField(max_length=255, blank=True)
    categories = models.ManyToManyField(Category, related_name="services", blank=True)
    hashtags = models.ManyToManyField(Hashtag, related_name="services", blank=True)
    keywords = models.ManyToManyField(Keyword, related_name="services", blank=True)

    def __str__(self):
        return self.name

    def get_categories(self):
        return "\n".join([p.categories for p in self.categories.all()])

    def get_hashtags(self):
        return "\n".join([p.hashtags for p in self.hashtags.all()])

    def get_keywords(self):
        return "\n".join([p.keywords for p in self.keywords.all()])


class Promotion(models.Model):
    product = models.ForeignKey(Product, related_name="promotions", on_delete=models.CASCADE, null=True, blank=True)
    service = models.ForeignKey(Service, related_name="promotions", on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=255, blank=True)
    categories = models.ManyToManyField(Category, related_name="promotions", blank=True)
    hashtags = models.ManyToManyField(Hashtag, related_name="promotions", blank=True)
    keywords = models.ManyToManyField(Keyword, related_name="promotions", blank=True)

    def __str__(self):
        return self.name

    def get_categories(self):
        return "\n".join([p.categories for p in self.categories.all()])

    def get_hashtags(self):
        return "\n".join([p.hashtags for p in self.hashtags.all()])

    def get_keywords(self):
        return "\n".join([p.keywords for p in self.keywords.all()])
