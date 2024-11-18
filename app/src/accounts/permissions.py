from rest_framework.permissions import BasePermission


class IsMerchantUser(BasePermission):
    """
    Allows access only to users who are associated with a merchant.
    """

    def has_permission(self, request, view):
        return hasattr(request.user, "merchant")


class IsMerchantHasProductOrService(BasePermission):
    """
    Allows access only to merchants who are associated with a product or service.
    """

    def has_permission(self, request, view):
        return hasattr(request.user.merchant, "product") | hasattr(request.user.merchant, "service")
