from django.contrib import admin

from accounts.models import User, Merchant


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
