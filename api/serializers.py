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
        fields = '__all__'


class ProjectSerializer(serializers.ModelSerializer):
    """
    serializer for Project model
    """

    class Meta:
        model = Project
        fields = '__all__'


class ListSerializer(serializers.ModelSerializer):
    """
    serializer for List model
    """

    class Meta:
        model = List
        fields = '__all__'


class CardSerializer(serializers.ModelSerializer):
    """
    serializer for Card model
    """

    class Meta:
        model = Card
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    """
    serializer for Comment model
    """

    class Meta:
        model = Comment
        fields = '__all__'
