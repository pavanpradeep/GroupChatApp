from rest_framework import serializers
from django.contrib.auth import authenticate
from chatapp.models import *


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('first_name', 'username', 'last_name', 'email', 'password')

    def create(self, validated_data):
        user = super(UserSerializer, self).create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


class GroupSerializer(serializers.ModelSerializer):
    members = UserSerializer(read_only=True, many=True)

    class Meta:
        model = Group
        fields = "__all__"


class GroupCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = [
            "name",
            # "members",
        ]

#     def create(self, validated_data):
#         group = super(groupCreateSerializer, self).create(validated_data)
#         group.save()
#         return group


class GroupMemberSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = [
            "members"
        ]
        # extra_kwargs = {'members': {'required': False}}

class MessageCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = GroupMessage
        fields = [
            "message",
        ]
        # extra_kwargs = {'group': {'required': False},
        # }

class GroupMessageSerializer(serializers.ModelSerializer):
    liked_by = UserSerializer(many=True)
    group = GroupSerializer()
    created_by = UserSerializer()

    class Meta:
        model = GroupMessage
        fields = "__all__"
    


# class MessageLikeSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = GroupMessage
#         fields = [
#             "liked_by",
#         ]