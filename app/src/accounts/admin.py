from django.contrib import admin

from accounts.models import User, Merchant, Product, Service, Promotion, Category, Hashtag, Keyword


class UserAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "email",
        "first_name",
        "last_name",
        "date_joined",
    )


admin.site.register(User, UserAdmin)


class MerchantAdmin(admin.ModelAdmin):
    list_display = ("user", "name")


admin.site.register(Merchant, MerchantAdmin)


class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "merchant", "name", "get_categories", "get_hashtags", "get_keywords")


admin.site.register(Product, ProductAdmin)


class ServiceAdmin(admin.ModelAdmin):
    list_display = ("id", "merchant", "name", "get_categories", "get_hashtags", "get_keywords")


admin.site.register(Service, ServiceAdmin)


class PromotionAdmin(admin.ModelAdmin):
    list_display = ("id", "product", "service", "name", "get_categories", "get_hashtags", "get_keywords")


admin.site.register(Promotion, PromotionAdmin)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name")


admin.site.register(Category, CategoryAdmin)


class HashtagAdmin(admin.ModelAdmin):
    list_display = ("id", "name")


admin.site.register(Hashtag, HashtagAdmin)


class KeywordAdmin(admin.ModelAdmin):
    list_display = ("id", "name")


admin.site.register(Keyword, KeywordAdmin)
