from rest_framework import permissions


class IsOwnerOrModerator(permissions.BasePermission):
    """
    Позволяет редактировать объект только владельцу или участнику группы 'moderators'.
    """

    def has_object_permission(self, request, view, obj):
        # Доступ всегда разрешён для безопасных методов (GET, HEAD, OPTIONS)
        if request.method in permissions.SAFE_METHODS:
            return True

        user = request.user

        # Модераторы могут редактировать
        if user.groups.filter(name="moderators").exists():
            return True

        # Владельцы могут редактировать свои объекты
        return obj.owner == user
