"""
Contains all views
"""

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.http import JsonResponse, HttpResponseForbidden, HttpResponseBadRequest
import json
import requests
from rest_framework.response import Response
from .login_config import config
from . import models
from django.contrib.auth import login, logout
from rest_framework import viewsets
from .serializers import UserSerializer,ProjectSerializer,ListSerializer,CardSerializer,CommentSerializer
from rest_framework.decorators import action
from rest_framework.views import APIView
from .permissions import IsUserEnabled, IsAdminOrProjectAdminOrReadOnly, IsAdmin, IsOwnerOrReadOnly, IsTeamMemberOrReadOnly_List, IsTeamMemberOrReadOnly_Project, IsTeamMemberOrReadOnly_Card
from rest_framework.permissions import IsAuthenticated

class LoginViewSet(viewsets.ModelViewSet):
    """
    A viewset that provides the standard actions like login, logout
    """
    queryset = models.User.objects.all()
    serializer_class = UserSerializer

    @action(detail=False, url_path='login', url_name='login-login')
    def login1(self, req):
        """
        It will redirect to oauth page
        from /api/login--> oauth
        """
        print("login1")
        url = f"https://channeli.in/oauth/authorise/?client_id={config['CLIENT_ID']}&redirect_uri={config['REDIRECT_URI']}&state={config['STATE_STRING']}"
        return HttpResponseRedirect(url)

    @action(detail=False, url_path='OAuth', url_name='login-OAuth')
    def login2(self, req):
        """
        exchange auth_code (received after login through channeli) with access_token which is further used to get the user's data
        """
        try:
            auth_code = req.GET['code']

        except:
            return HttpResponseBadRequest()

        params = {
            'client_id': config['CLIENT_ID'],
            'client_secret': config['CLIENT_SECRET'],
            'grant_type': 'authorization_code',
            'redirect_uri': config['REDIRECT_URI'],
            'code': auth_code,
        }

        res = requests.post("https://channeli.in/open_auth/token/", data=params)

        if (res.status_code == 200):
            access_token = res.json()['access_token']
            refresh_token = res.json()['refresh_token']
        else:
            return HttpResponseBadRequest()

        header = {
            "Authorization": "Bearer " + access_token,
        }

        res1 = requests.get("https://channeli.in/open_auth/get_user_data/", headers=header)
        data_final = res1.json()

        isMaintainer = False
        for role in data_final['person']['roles']:
            print(role['role'])
            if (role['role'] == 'Maintainer'):
                isMaintainer = True

        if not isMaintainer:
            return HttpResponse("You are not a maintainer")

        try:
            user = models.User.objects.get(enrollment_no=data_final['username'])

        except:
            user_name = data_final['person']['fullName']
            ern = data_final['username']
            isAdmin = False
            isEnabled = True
            user = models.User(enrollment_no=ern, User_name=user_name, admin=isAdmin, enabled=isEnabled)
            print("saving")
            user.save()
            print("saved")
        login(request=req, user=user)
        return HttpResponse("done!")

class UserViewSet(viewsets.ModelViewSet):
    queryset = models.User.objects.all()
    serializer_class = UserSerializer

    # @action(methods= ['GET'], detail=False, url_path='myprojects', url_name='user-myprojects')
    # def projects(self, request):
    #     projects_data=ProjectSerializer(request.user.member.all(), many=True)
    #     return Response(projects_data.data)
    #
    # @action(methods= ['GET'],detail=False, url_path='mycards', url_name='user-mycards')
    # def cards(self, request):
    #     cards_data=CardSerializer(request.user.mycards.all(), many=True)
    #     return Response(cards_data.data)

    queryset = models.User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            self.permission_classes = [IsUserEnabled, IsAuthenticated]
        else:
            self.permission_classes = [IsAuthenticated,IsUserEnabled, IsAdmin]
        return super(UserViewSet, self).get_permissions()

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = models.Project.objects.all()
    serializer_class = ProjectSerializer

    # @action(methods=['GET'], detail=False, url_path='list', url_name='project-list')
    # def list_project(self, request):
    #     proj= models.Project.objects.all()
    #     proj_data=ProjectSerializer(proj, many=True)
    #     return Response(proj_data.data)
    #
    # @action(methods=['POST'], detail=False, url_path='create', url_name='project-create')
    # def create_project(self, request):
    #     proj_data=ProjectSerializer(proj, many=True)
    #     return Response(proj_data.data)

    # def perform_create(self, serializer):
    #     serializer.save()

    def get_permissions(self):
        if self.request.method == 'GET' or self.request.method == 'POST':
            self.permission_classes = [IsUserEnabled, IsAuthenticated]
        else:
            self.permission_classes = [IsAuthenticated,IsUserEnabled, IsAdminOrProjectAdminOrReadOnly]
        return super(ProjectViewSet, self).get_permissions()


class ListViewSet(viewsets.ModelViewSet):
    queryset = models.List.objects.all()
    serializer_class = ListSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            self.permission_classes = [IsUserEnabled, IsAuthenticated]
        else:
            self.permission_classes = [IsAuthenticated,IsUserEnabled, IsTeamMemberOrReadOnly_List]

        return super(ListViewSet, self).get_permissions()


class CardViewSet(viewsets.ModelViewSet):

    queryset = models.Card.objects.all()
    serializer_class = CardSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            self.permission_classes = [IsUserEnabled, IsAuthenticated]
        else:
            self.permission_classes = [IsAuthenticated,IsUserEnabled, IsTeamMemberOrReadOnly_Card]

        return super(CardViewSet, self).get_permissions()

class CommentViewSet(viewsets.ModelViewSet):

    queryset = models.Comment.objects.all()
    serializer_class = CommentSerializer

    def get_permissions(self):
        if self.request.method == 'GET' or self.request.method == 'POST':
            self.permission_classes = [IsUserEnabled, IsAuthenticated]
        else:
            self.permission_classes = [IsAuthenticated,IsUserEnabled, IsOwnerOrReadOnly]
        return super(CommentViewSet, self).get_permissions()