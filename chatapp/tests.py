import datetime
from django.test import TestCase, Client
from rest_framework.authtoken.models import Token
from chatapp.apps import ChatappConfig
from django.urls import reverse
from chatapp.models import *
from rest_framework.test import APIClient


class ObjectsCreation(object):
    def setUp(self):
        self.client = APIClient()

        # admin user
        self.user1 = User.objects.create(
            first_name="firstname1",
            last_name="lastname1",
            username="user1",
            email="user1@gmail.com",
            is_superuser=True,
            is_staff=True,
        )
        self.user1.set_password("password1")
        self.user1.save()
        self.token1 = Token.objects.get(user=self.user1)

        # normal user
        self.user2 = User.objects.create(
            first_name="firstname2",
            last_name="lastname2",
            username="user2",
            email="user2@gmail.com",
        )
        self.user2.set_password("password")
        self.user2.save()
        self.token2 = Token.objects.get(user=self.user2)

        # Groups
        self.group1 = Group.objects.create(name="Group 1", created_by=self.user1)
        self.group2 = Group.objects.create(name="Group 2", created_by=self.user1)

        # GroupMessages
        self.group_message1 = GroupMessage.objects.create(message="Hi how are you?", group=self.group1, created_by=self.user1)
        self.group_message2 = GroupMessage.objects.create(message="Hi, I am Fine.How are you?", group=self.group1, created_by=self.user1)

        # user1 login
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token1.key)


class TestChatApp(ObjectsCreation, TestCase):
    def test_app_file(self):
        self.assertEqual(ChatappConfig.name, "chatapp")

    # Group Testcases

    def test_creategroup(self):
        response = self.client.post(reverse("chatapp:create_new_group"), data={"name": "Group 3"})
        self.assertEqual(response.status_code, 201)

    def test_groupList(self):
        response = self.client.get(reverse("chatapp:groups_list"))
        self.assertEqual(response.status_code, 200)

    def test_editgroup(self):
        response = self.client.post(reverse("chatapp:update_group", kwargs={"id":self.group2.id}), data={"name": "Group 2 updated name"})
        self.assertEqual(response.status_code, 200)

    def test_deletegroup(self):
        response = self.client.post(reverse("chatapp:delete_group", kwargs={"id":self.group2.id}))
        self.assertEqual(response.status_code, 200)

    
    # users testcases

    def test_createuser(self):
        data = {"first_name":"firstname3",
                "last_name":"lastname3",
                "username":"user3",
                "email":"user3@gmail.com",
                "password":"test3",
                }
        response = self.client.post(reverse("chatapp:create_new_user"), data=data)
        self.assertEqual(response.status_code, 201)

    def test_userList(self):
        response = self.client.get(reverse("chatapp:user_list"))
        self.assertEqual(response.status_code, 200)

    def test_edituser(self):
        data = {"first_name":"firstname3333333",
                "last_name":"lastname333333",
                "username":self.user2.username,
                "password":self.user2.password,
                "email":self.user2.email,
                }
        response = self.client.post(reverse("chatapp:update_user", kwargs={"id":self.user2.id}), data=data)
        self.assertEqual(response.status_code, 200)

    def test_deleteuser(self):
        response = self.client.post(reverse("chatapp:delete_user", kwargs={"id":self.user2.id}))
        self.assertEqual(response.status_code, 200)


    # GroupMember Testcases

    def test_addgroupmember(self):
        response = self.client.post(reverse("chatapp:add_user_to_group", kwargs={"id":self.group1.id}), data={"members": [self.user1.id]})
        self.assertEqual(response.status_code, 201)

    def test_removegroupmember(self):
        response = self.client.post(reverse("chatapp:remove_user_from_group", kwargs={"id":self.group1.id}), data={"members": [self.user1.id]})
        self.assertEqual(response.status_code, 200)


    # GroupMessages Testcases

    def test_groupmessages(self):
        response = self.client.get(reverse("chatapp:group_messages_list"))
        self.assertEqual(response.status_code, 200)

    def test_groupmessage_create(self):
        response = self.client.post(reverse("chatapp:create_group_message", kwargs={"id":self.group1.id}), data={"message": "Welcome to the Group"})
        self.assertEqual(response.status_code, 201)

    # GroupMessageLike Testcases

    def test_groupmessagelike_create(self):
        response = self.client.post(reverse("chatapp:create_group_like", kwargs={"group_id":self.group1.id,"msg_id":self.group_message1.id}))
        self.assertEqual(response.status_code, 201)

