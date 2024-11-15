from django.contrib import admin

from accounts.models import User


class UserAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "email",
        "first_name",
        "last_name",
        "date_joined",
    )


admin.site.register(User, UserAdmin)
