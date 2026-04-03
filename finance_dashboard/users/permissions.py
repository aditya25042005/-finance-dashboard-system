from rest_framework.permissions import BasePermission


class Admin(BasePermission):
    message = "Only admin users can perform this action."

    def has_permission(self, request, view):
        return (
            getattr(request, "jwt_authenticated", False)
            and getattr(request.users, "role", None) == "admin"
        )


class Analyst_Admin(BasePermission):
    message = "Only analyst or admin users can perform this action."

    def has_permission(self, request, view):
        return (
            getattr(request, "jwt_authenticated", False)
            and getattr(request.users, "role", None) in ["analyst", "admin"]
        )


class Viewer_Analyst_Admin(BasePermission):
    message = "Only viewer, analyst, or admin users can perform this action."

    def has_permission(self, request, view):
        return (
            getattr(request, "jwt_authenticated", False)
            and getattr(request.users, "role", None) in ["viewer", "analyst", "admin"]
        )