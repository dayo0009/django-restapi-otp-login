from rest_framework import permissions
from django.shortcuts import redirect


class UserCustomAuthentication(permissions.BasePermission):
    message = "User not authorize"

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return True
