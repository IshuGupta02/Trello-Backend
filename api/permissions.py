"""
All types of permissions required are defined here
"""

from rest_framework import permissions
from .models import User, List, Comment, Project, Card

class IsUserEnabled(permissions.BasePermission):
    """
    If a user is not Enabled, False will be returned
    """

    def has_permission(self, request, view):
        if not request.user.enabled:
            return False
        return True

class IsAdminOrProjectAdminOrReadOnly(permissions.BasePermission):
    """
    Project Settings can be changed only by project admins or the app admins
    All others can only see the settings
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        for p in User.object.all().iterator():
            if p.admin and p == request.User:
                return True

        for member in obj.admins:
            if request.User==member
                return True
        return False

class IsTeamMemberOrReadOnly(permissions.BasePermission):
    """
    Changing anything in a project is only allowed to project members
    All others can only see the project
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        for member in obj.members:
            if member == request.User
                return True
        return False


class IsAdmin(permissions.BasePermission):
    """
    App admins have extra powers of changing any app admin to normal member or vice versa
    """
    def has_permission(self, request, view):
        for p in User.object.all().iterator():
            if p.admin and p == request.User:
                return True
        return False

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Only owners of a comment can change it
    All other can only see the comment
    """

    def has_object_permission(self, request, view, obj):
        return obj.User == request.User
