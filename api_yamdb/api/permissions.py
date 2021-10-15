from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_staff
                or (request.user.is_authenticated
                    and request.user.role == 'admin')
                )


class IsAdmin(permissions.BasePermission):

    def has_permission(self, request, view):
        return (request.user.is_staff
                or (request.user.is_authenticated
                    and request.user.role == 'admin')
                )


class IsAuthorModeratorAdminOrReadOnly(permissions.BasePermission):
    ROLE = ('moderator', 'admin')

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or (request.user.is_authenticated
                    and request.user.role in self.ROLE)
                or request.user.is_staff
                or obj.author == request.user)
