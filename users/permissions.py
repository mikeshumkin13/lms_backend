from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsModerator(BasePermission):
    """Пользователь — модератор (по группе)"""

    def has_permission(self, request, view):
        return request.user and request.user.groups.filter(name="moderators").exists()


class IsOwnerOrModerator(BasePermission):
    """Пользователь — владелец объекта или модератор"""

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            if request.user.groups.filter(name="moderators").exists():
                return True
            return obj.owner == request.user
        return False
