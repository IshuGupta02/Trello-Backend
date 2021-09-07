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
from .permissions import IsUserEnabled, IsAdminOrProjectAdminOrReadOnly, IsAdmin, IsOwnerOrReadOnly, IsTeamMemberOrReadOnly_List, IsTeamMemberOrReadOnly_Project, IsTeamMemberOrReadOnly_Card, Not_allowed
from rest_framework.permissions import IsAuthenticated, AllowAny


class LoginViewSet(viewsets.ModelViewSet):
    """
    A viewset that provides the standard actions like login, logout
    1. if user exists--> login
    2. if new user comes--> create a new User Object and login
    3. logout
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
        active=True
        for role in data_final['person']['roles']:
            print(role['role'])
            if (role['role'] == 'Maintainer'):
                isMaintainer = True
                if(role['activeStatus']!='ActiveStatus.IS_ACTIVE'):
                    active=False

        # if not active:
        #     try:
        #         models.User.objects.filter(enrollment_no=data_final['username']).delete()
        #     except:
        #
        #     return JsonResponse({'status': 'you are not active anymore'})

        if not isMaintainer:
            return JsonResponse({'status': 'you are not a maintainer'})


        print(data_final)

        try:
            user = models.User.objects.get(enrollment_no=data_final['username'])
            # models.User.objects.filter(enrollment_no=data_final['username']).delete()

        except:
            user_name = data_final['person']['fullName']
            email_id=data_final['contactInformation']['emailAddress']
            ern = data_final['username']
            isAdmin = False
            isEnabled = True
            user = models.User(enrollment_no=ern, User_name=user_name, admin=isAdmin, enabled=isEnabled, email=email_id)
            print("saving")
            user.save()
            print("saved")
        login(request=req, user=user)
        return HttpResponse("done!")

    @action(methods=['GET'], detail=False, url_path='logout', url_name='login-logout')
    def logout_(self, request):
        """
        logout user
        """
        if request.user.is_authenticated:
            logout(request)
            return JsonResponse({'status': 'successful'})
        else:
            return HttpResponseForbidden()

class UserViewSet(viewsets.ModelViewSet):
    """
    1. get all users data
    2. update a user's Admin Status
    3. update a user's Enabled Status
    """
    queryset = models.User.objects.all()
    serializer_class = UserSerializer

    # @action(methods= ['GET'], detail=False, url_path='myprojects', url_name='user-myprojects')
    # def projects(self, request):
    #     print(request.user)
    #     projects_data=ProjectSerializer(request.user.member.all(), many=True)
    #     return Response(projects_data.data)

    # @action(methods= ['GET'],detail=False, url_path='mycards', url_name='user-mycards')
    # def cards(self, request):
    #     cards_data=CardSerializer(request.user.mycards.all(), many=True)
    #     return Response(cards_data.data)

    def get_permissions(self):
        """
        everbody can get details of users but only admins can enable/disable, change to admin/remove from admin
        """
        if self.request.method == 'GET':
            self.permission_classes = [IsUserEnabled, IsAuthenticated]
        elif self.request.method == 'POST' or self.request.method == 'DELETE':
            self.permission_classes = [Not_allowed]
        else:
            self.permission_classes = [IsAuthenticated,IsUserEnabled, IsAdmin]
        return super(UserViewSet, self).get_permissions()

    @action(methods=['GET'], detail=False, url_path='info', url_name='user-info')
    def info(self, request):
        # print(request.user)
        # # user_data=models.User.objects.get(request.user)
        # return Response("user")

        info = UserSerializer(request.user)
        return Response(info.data)

class ProjectViewSet(viewsets.ModelViewSet):
    """
    1. get all projects
    2. update a project- members, admins, wiki, project_name, due_date
    3. delete a project
    4. create new project
    """
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
        """
        1. everyone can get information about any project or create a new project
        2. only project admins or app admins can add or remove members, project_admins, change due_date, edit wiki, etc
        """
        if self.request.method == 'GET' or self.request.method == 'POST':
            self.permission_classes = [IsUserEnabled, IsAuthenticated]
        else:
            self.permission_classes = [IsAuthenticated,IsUserEnabled, IsAdminOrProjectAdminOrReadOnly]
        return super(ProjectViewSet, self).get_permissions()

class ListViewSet(viewsets.ModelViewSet):
    """
    1. get all lists
    2. create a new list in a project
    3. update a list- list_name
    4. delete a list
    """
    queryset = models.List.objects.all()
    serializer_class = ListSerializer

    def get_permissions(self):
        """
        anyone can get information about any list
        only project members can create/update/delete a list
        """
        if self.request.method == 'GET':
            self.permission_classes = [IsUserEnabled, IsAuthenticated]
        else:
            self.permission_classes = [IsAuthenticated,IsUserEnabled, IsTeamMemberOrReadOnly_List]

        return super(ListViewSet, self).get_permissions()

class CardViewSet(viewsets.ModelViewSet):
    """
    1. get all cards
    2. create a new card in a project
    3. update a card- card_name, assigned_to,description
    4. delete a card
    """

    queryset = models.Card.objects.all()
    serializer_class = CardSerializer

    def get_permissions(self):
        """
        anyone can get information about any card
        only project members can create/update/delete a card
        """
        if self.request.method == 'GET':
            self.permission_classes = [IsUserEnabled, IsAuthenticated]
        else:
            self.permission_classes = [IsAuthenticated,IsUserEnabled, IsTeamMemberOrReadOnly_Card]

        return super(CardViewSet, self).get_permissions()

class CommentViewSet(viewsets.ModelViewSet):
    """
    1. get all comments
    2. update a comment
    3. create a comment
    """

    queryset = models.Comment.objects.all()
    serializer_class = CommentSerializer

    def get_permissions(self):
        """
        everyone can view comments/ create a new comment
        only comment creator can change it
        """
        if self.request.method == 'GET' or self.request.method == 'POST':
            self.permission_classes = [IsUserEnabled, IsAuthenticated]
        else:
            self.permission_classes = [IsAuthenticated,IsUserEnabled, IsOwnerOrReadOnly]
        return super(CommentViewSet, self).get_permissions()