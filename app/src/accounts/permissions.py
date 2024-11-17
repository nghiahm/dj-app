from rest_framework.permissions import BasePermission


class IsMerchantUser(BasePermission):
    """
    Allows access only to users who are associated with a merchant.
    """

    def has_permission(self, request, view):
        return hasattr(request.user, "merchant")
