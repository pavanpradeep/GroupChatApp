from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.urls import reverse
from django.conf import settings
from django.contrib.auth.decorators import login_required
from chatapp.models import *
from django.contrib.auth import authenticate
from chatapp.forms import *
from django.http.response import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import get_list_or_404, get_object_or_404

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .serializer import *
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django.db.models import Q
from rest_framework import status

def is_admin_user(function):
    def check_user(request, *args, **kwargs):
        if request.user.is_staff:
            return function(request, *args, **kwargs)
        return HttpResponse(status=401)

    return check_user

def login_view(request):
    error_message = ''
    form = UserLoginForm()
    if request.user.is_authenticated:
        return redirect(reverse('chatapp:users_list'))

    if request.method == "POST":
        form = UserLoginForm(request.POST)
        if form.is_valid():
            user = authenticate(username=request.POST.get('username').lower(), password=request.POST.get('password'))
            print(user,"user")
            if user is not None:
                login(request, user)
                return redirect(reverse('chatapp:users_list'))
        error_message = 'Invalid Username or Password'

    print(request.POST, error_message)
    return render(request, "login.html", {'form': form,'error':error_message})



@login_required
def logout_view(request):
    logout(request)
    return redirect(reverse('chatapp:login_view'))


@login_required
def users_list(request):
    if request.method == 'GET':
        user_list = User.objects.all()
        return render(request, "users_list.html", {'user_list': user_list})

@is_admin_user
def get_user_object(request):
    data = {}
    if request.GET.get('user_id', ""):
        user_obj = User.objects.get(id=int(request.GET.get('user_id')))
        data = user_obj.as_dict()
    return JsonResponse(data)

@is_admin_user
def user_operations(request):
    task = request.POST.get('task', None)
    user_id = request.POST.get('user_id', None)
    if user_id and task == 'user_delete':
        obj = get_object_or_404(User,pk=int(user_id))
        obj.delete()
    elif user_id and task == 'user_edit':
        obj = get_object_or_404(User,pk=int(user_id))
        User.objects.filter(id=int(user_id)).update(email=request.POST.get('email'), username=request.POST.get('username'), first_name=request.POST.get('first_name'), last_name=request.POST.get('last_name'))
    elif task == 'user_create':
        User.objects.create(email=request.POST.get('email'), username=request.POST.get('username'), first_name=request.POST.get('first_name'), last_name=request.POST.get('last_name'))
    return redirect(reverse('chatapp:users_list'))





# Rest API Functions

class UserLogin(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        },status = status.HTTP_200_OK)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def user_logout(request):
    if request.method == "POST":
        # simply delete the token to force a login
        request.user.auth_token.delete()
        data = {"message":"User Created SUccessfully"}
    return Response(data,status=status.HTTP_200_OK)


@api_view(["GET"])
@permission_classes([IsAuthenticated,IsAdminUser])
def user_list(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    data = {"users_list":serializer.data}
    return Response(data,status = status.HTTP_200_OK)



@api_view(["POST"])
@permission_classes([IsAuthenticated,IsAdminUser])
def create_new_user(request):
    if request.method == "POST":
        serializer = UserSerializer(data=request.POST)
        if serializer.is_valid():
            serializer.save()
            data = {"message":"User Created SUccessfully"}
            Status = status.HTTP_201_CREATED
        else:
            data = {"message":"User Creation Failed","errors":serializer.errors}
            Status = status.HTTP_400_BAD_REQUEST
    return Response(data,status = Status)


@api_view(["POST"])
@permission_classes([IsAuthenticated,IsAdminUser])
def update_user(request, id):
    user = User.objects.get(id=id)
    if request.method == "POST":
        serializer = UserSerializer(user, data=request.POST)
        if serializer.is_valid():
            serializer.save()
            data = {"message":"User Updated SUccessfully"}
            Status = status.HTTP_200_OK
        else:
            data = {"message":"User Updation Failed","errors":serializer.errors}
            Status = status.HTTP_400_BAD_REQUEST
    return Response(data,status = Status)


@api_view(["POST"])
@permission_classes([IsAuthenticated,IsAdminUser])
def delete_user(request, id):
    user = User.objects.filter(id=id)
    if user.exists():
        user.delete()
        data = {"message":"User Deleted SUccessfully"}
        Status = status.HTTP_200_OK
    else:
        data = {"message":"User Doesnot Exists"}
        Status = HTTP_400_BAD_REQUEST
    return Response(data,status = Status)


# Groups

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def groups_list(request):
    user = request.user
    if user.is_staff:
        groups = Group.objects.all()
    else:
        groups = Group.objects.filter(Q(created_by=request.user) | Q(members__email=user.email))
    serializer = GroupSerializer(groups, many=True)
    data = {"groups_list":serializer.data}
    return Response(data,status = status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_new_group(request):
    user = request.user
    if request.method == "POST":
        serializer = GroupCreateSerializer(data=request.POST)
        if serializer.is_valid():
            group = serializer.save()
            group.members.add(user)
            group.created_by = user
            group.save()
            data = {"message":"Group Created SUccessfully"}
            Status = status.HTTP_201_CREATED
        else:
            data = {"message":"Group Creation Failed","errors":serializer.errors}
            Status = HTTP_400_BAD_REQUEST
    return Response(data, status=Status)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def update_group(request, id):
    group = Group.objects.get(id=id)
    if request.method == "POST":
        if group.created_by == request.user:
            serializer = GroupCreateSerializer(group, data=request.POST)
            if serializer.is_valid():
                serializer.save()
                data = {"message":"Group data Updated SUccessfully"}
                Status = status.HTTP_200_OK
            else:
                data = {"message":"Group data Updation Failed","errors":serializer.errors}
                Status = HTTP_400_BAD_REQUEST
        else:
            data = {"message":"You don't have permission to Edit"}
            Status = HTTP_400_BAD_REQUEST
    return Response(data, status=Status)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def delete_group(request, id):
    group = Group.objects.get(id=id)
    if group.created_by == request.user:
        if group:
            group.delete()
            data = {"message":"Group Deleted SUccessfully"}
            Status = status.HTTP_200_OK
        else:
            data = {"message":"Group Doesnot Exists"}
            Status = HTTP_400_BAD_REQUEST
    else:
        data = {"message":"You don't have permission to delete"}
        Status = HTTP_400_BAD_REQUEST
    return Response(data, status=Status)



@api_view(["POST"])
@permission_classes([IsAuthenticated])
def add_user_to_group(request, id):
    if request.method == "POST":
        group = Group.objects.get(id=id)
        if group.created_by == request.user:
            serializer = GroupMemberSerializer(data=request.POST)
            if serializer.is_valid():
                members_list = serializer.data["members"]
                print(members_list)
                group.members.add(*members_list)
                group.save()
                data = {"message":"Added User SUccessfully"}
                Status = status.HTTP_201_CREATED
            else:
                data = {"message":"Adding User Failed","errors":serializer.errors}
                Status = HTTP_400_BAD_REQUEST
        else:
            data = {"message":"You don't have permission to add user to this group"}
            Status = HTTP_400_BAD_REQUEST
    return Response(data, status=Status)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def remove_user_from_group(request, id):
    if request.method == "POST":
        group = Group.objects.get(id=id)
        if group.created_by == request.user:
            serializer = GroupMemberSerializer(data=request.POST)
            if serializer.is_valid():
                members_list = serializer.data["members"]
                print(members_list)
                group.members.remove(*members_list)
                group.save()
                Status = status.HTTP_200_OK
                data = {"message":"Removed User SUccessfully"}
            else:
                Status = HTTP_400_BAD_REQUEST
                data = {"message":"Removing User Failed","errors":serializer.errors}
        else:
            Status = HTTP_400_BAD_REQUEST
            data = {"message":"You don't have permission to add user to this group"}
    return Response(data, status=Status)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_group_message(request, id):
    user = request.user
    group = Group.objects.get(id=id)
    if request.method == "POST":
        serializer = MessageCreateSerializer(data=request.POST)
        if serializer.is_valid():
            group = serializer.save(created_by=user, group=group)
            data = {"message":"Message Created SUccessfully"}
            Status = status.HTTP_201_CREATED
        else:
            data = {"message":"Message Creation Failed","errors":serializer.errors}
            Status = HTTP_400_BAD_REQUEST
    return Response(data, status=Status)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_group_like(request, group_id, msg_id):
    user = request.user
    try:
        group = Group.objects.get(id=group_id)
        message = GroupMessage.objects.get(group=group, id=msg_id)
        message.liked_by.add(user)
        data = {"message":"Like Created SUccessfully"}
        Status = status.HTTP_201_CREATED
    except Exception as e:
        data = {"message":"Like creattion Failed","errors":str(e)}
        Status = HTTP_400_BAD_REQUEST
    return Response(data,status=Status)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def group_messages_list(request):
    group_msg = GroupMessage.objects.all()
    serializer = GroupMessageSerializer(group_msg, many=True)
    data = {"group_messages":serializer.data}
    return Response(data,status = status.HTTP_200_OK)