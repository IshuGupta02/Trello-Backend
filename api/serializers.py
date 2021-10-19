"""
contains all serializers used in the api
"""

from rest_framework import serializers
from .models import User, List, Comment, Project, Card

class UserSerializer1(serializers.ModelSerializer):
    """
    serializer for User model - restricted data
    """

    class Meta:
        model = User
        fields = ['id', 'enrollment_no', 'User_name', 'email', 'profile']
        read_only_fields = ['id', 'enrollment_no', 'User_name', 'email', 'profile']


class ProjectSerializer_card(serializers.ModelSerializer):
    """
    serializer for Project model
    """

    class Meta:
        model = Project
        fields = ['id', 'Project_name']

class ListSerializer_card(serializers.ModelSerializer):
    """
    serializer for List model
    """

    Project= ProjectSerializer_card(read_only=True)

    class Meta:
        model = List
        fields = ['id', 'List_name', 'Project']
        read_only_fields = ['id']


class CardSerializer(serializers.ModelSerializer):
    """
    serializer for Card model
    """

    # assigned=UserSerializer1(many=True, read_only=True)

    class Meta:
        model = Card
        fields = ['id', 'Card_name', 'List', 'assigned', 'description']
        read_only_fields = ['id']

class CardSerializer2(serializers.ModelSerializer):
    """
    serializer for Card model
    """

    assigned=UserSerializer1(many=True, read_only=True)

    class Meta:
        model = Card
        fields = ['id', 'Card_name', 'List', 'assigned', 'description']
        read_only_fields = ['id']


class CardSerializer1(serializers.ModelSerializer):
    """
    serializer for Card model
    """

    assigned=UserSerializer1(many=True, read_only=True)
    List= ListSerializer_card(read_only=True)

    class Meta:
        model = Card
        fields = ['id', 'Card_name', 'List', 'assigned', 'description']
        read_only_fields = ['id']


class ListSerializer(serializers.ModelSerializer):
    """
    serializer for List model
    """

    cardsoflist = CardSerializer2(many=True, read_only=True)

    class Meta:
        model = List
        fields = ['id', 'List_name', 'Project', 'cardsoflist']
        read_only_fields = ['id']


class ProjectSerializer(serializers.ModelSerializer):
    """
    serializer for Project model
    """

    listsassociated = ListSerializer(many=True, read_only=True)
    # members = UserSerializer1(many=True, read_only=True)

    # card = CardSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = ['id', 'Project_name', 'wiki', 'date_created', 'due_date', 'members', 'admins', 'listsassociated']
        read_only_fields = ['id', 'date_created']


class CommentSerializer(serializers.ModelSerializer):
    """
    serializer for Comment model
    """

    class Meta:
        model = Comment
        fields = ['id', 'User', 'Card', 'date_created', 'Comment']
        read_only_fields = ['id', 'User', 'date_created', 'Card']

class CommentSerializer1(serializers.ModelSerializer):
    """
    serializer for Comment model
    """

    User = UserSerializer1(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'User', 'Card', 'date_created', 'Comment']
        read_only_fields = ['id', 'User', 'date_created', 'Card']


class CardCommentSerializer(serializers.ModelSerializer):
    """
    for accessing with comments of a particular card
    """

    commentsofcards= CommentSerializer1(many=True, read_only=True)

    class Meta:
        model = Card
        fields = ['id', 'Card_name', 'List', 'assigned', 'description']
        read_only_fields = ['id']


class ProjectSerializer1(serializers.ModelSerializer):
    """
    serializer for Project model
    """

    listsassociated = ListSerializer(many=True, read_only=True)
    members = UserSerializer1(many=True, read_only=True)
    admins= UserSerializer1(many=True, read_only=True)

    # card = CardSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = ['id', 'Project_name', 'wiki', 'date_created', 'due_date', 'members', 'admins', 'listsassociated']
        read_only_fields = ['id', 'date_created']
        

class UserSerializer(serializers.ModelSerializer):
    """
    serializer for User model
    """

    mycards= CardSerializer1(many= True, read_only=True)
    member= ProjectSerializer1(many=True, read_only=True)
    mycomments=CommentSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'enrollment_no', 'User_name', 'admin', 'enabled', 'mycards', 'member', 'mycomments', 'email', 'profile']
        read_only_fields = ['id', 'enrollment_no', 'User_name', 'email', 'profile']

