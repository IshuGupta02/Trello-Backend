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
        print(request.user)
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
        for p in User.objects.all().iterator():
            if p.admin and p == request.user:
                return True
        for member in obj.admins.iterator():
            if request.user==member:
                return True
        return False

class IsTeamMemberOrReadOnly_Project(permissions.BasePermission):
    """
    Changing anything in a project is only allowed to project members
    All others can only see the project
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        for p in User.objects.all().iterator():
            if p.admin and p == request.user:
                return True
        for member in obj.members:
            if member == request.user:
                return True
        return False

class IsTeamMemberOrReadOnly_List(permissions.BasePermission):
    """
    Changing anything in a project is only allowed to project members
    All others can only see the project
    """

    def has_object_permission(self, request, view, obj):
        print(request.method)
        if request.method in permissions.SAFE_METHODS:
            print("safe")
            return True
        for p in User.objects.all().iterator():
            if p.admin and p == request.user:
                print("admin")
                return True
        for member in obj.Project.members.all():
            if member == request.user:
                print("member")
                return True
        return False

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.method == 'POST':
            for p in User.objects.all().iterator():
                if p.admin and p == request.user:
                    return True
            for project in Project.objects.all().iterator():
                if project.id == request.data.get('Project'):
                    for member in project.members.iterator():
                        if request.user == member:
                            return True
        else:
            return True
        return False

class IsTeamMemberOrReadOnly_Card(permissions.BasePermission):
    """
    Changing anything in a project is only allowed to project members
    All others can only see the project
    """

    def has_object_permission(self, request, view, obj):
        # print(obj.List.Project.members.all())
        print(request.method)
        if request.method in permissions.SAFE_METHODS:
            print("safe")
            return True
        for p in User.objects.all().iterator():
            # print("loop1", p)
            if p.admin and p == request.user:
                print("admin")
                return True
        for member in obj.List.Project.members.all().iterator():
            print("loop2", member)
            if member == request.user:
                return True
        return False

    def has_permission(self, request, view):
        print("checking")
        if request.method in permissions.SAFE_METHODS:
            return True
        print(request.method, request.data)
        # print(request.data.get('List'))
        if request.method == 'POST':
            print(request.data.get('List'))
            for p in User.objects.all().iterator():
                if p.admin and p == request.user:
                    print("admin")
                    return True
            for list in List.objects.all().iterator():
                print(list.id)
                if list.id == request.data.get('List'):
                    # print(list.id)
                    # print(request.data.get('List'))
                    print("inside")
                    for member in list.Project.members.iterator():
                        print("member")
                        if member.id==request.user.id:
                            return True
        else:
            return True
        return False

class IsAdmin(permissions.BasePermission):
    """
    App admins have extra powers of changing any app admin to normal member or vice versa
    """
    def has_permission(self, request, view):
        print("checking permissions")
        for p in User.objects.all().iterator():
            if p.admin and p == request.user:
                return True
        return False

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Only owners of a comment can change it
    All other can only see the comment
    """

    def has_object_permission(self, request, view, obj):
        return obj.User == request.user

class Not_allowed(permissions.BasePermission):
    """
    always returns false
    """

    def has_permission(self, request, view):
        return False
