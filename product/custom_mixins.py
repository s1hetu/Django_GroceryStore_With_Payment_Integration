from django.core.exceptions import PermissionDenied


class UserIsCustomerMixin:
    def dispatch(self, request, *args, **kwargs):
        user_type = request.user.is_staff
        if user_type:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)


class UserIsSellerMixin:
    def dispatch(self, request, *args, **kwargs):
        user_type = request.user.is_staff
        if not user_type:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)
