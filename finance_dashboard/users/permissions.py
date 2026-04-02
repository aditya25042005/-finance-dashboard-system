from rest_framework.permissions import BasePermission


class Admin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "admin"


class Analyst_Admin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ["analyst", "admin"]


class Viewer_Analyst_Admin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ["viewer", "analyst", "admin"]