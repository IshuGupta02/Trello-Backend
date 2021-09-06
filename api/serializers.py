"""
contains all serializers used in the api
"""

from rest_framework import serializers
from .models import User, List, Comment, Project, Card


class UserSerializer(serializers.ModelSerializer):
    """
    serializer for User model
    """

    class Meta:
        model = User
        fields = ['id','enrollment_no','User_name','admin','enabled']


class ProjectSerializer(serializers.ModelSerializer):
    """
    serializer for Project model
    """

    class Meta:
        model = Project
        fields = ['id','Project_name','wiki','date_created','due_date','members','admins']


class ListSerializer(serializers.ModelSerializer):
    """
    serializer for List model
    """

    class Meta:
        model = List
        fields = ['id','List_name','Project']


class CardSerializer(serializers.ModelSerializer):
    """
    serializer for Card model
    """

    class Meta:
        model = Card
        fields =['id','Card_name','List','assigned','description']


class CommentSerializer(serializers.ModelSerializer):
    """
    serializer for Comment model
    """

    class Meta:
        model = Comment
        fields = ['id','User','Card','date_created','Comment']
