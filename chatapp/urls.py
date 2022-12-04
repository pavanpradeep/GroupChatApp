from django.urls import path, include
from chatapp import views
from rest_framework.authtoken import views as restframework_views


app_name = 'chatapp'


urlpatterns = [
    path('', views.login_view, name="login_view"),
    path('logout/', views.logout_view, name='logout_view'),
    path('users/list/', views.users_list, name='users_list'),
    path('get-user-info/', views.get_user_object, name='get_user_object'),
    path("user/operations/", views.user_operations, name="user_operations"),

    # Rest API

    # login and logout
    path("api-token-auth/", views.UserLogin.as_view(), name="user_login"),
    path("logout/", views.user_logout, name="user_logout"),

    # users
    path("create/user/",views.create_new_user, name="create_new_user"),
    path("edit/user/<int:id>", views.update_user, name="update_user"),
    path("delete/user/<int:id>", views.delete_user, name="delete_user"),
    path("user/list", views.user_list, name="user_list"),

    # Groups
    path("create/group/",views.create_new_group, name="create_new_group"),
    path("update/group/<int:id>", views.update_group, name="update_group"),
    path("delete/group/<int:id>", views.delete_group, name="delete_group"),
    path("groups/list", views.groups_list, name="groups_list"),
    path("<int:id>/add/user/", views.add_user_to_group, name="add_user_to_group"),
    path("<int:id>/remove/user/", views.remove_user_from_group, name="remove_user_from_group"),

    # Group Messages
    path("groups/messages/list", views.group_messages_list, name="group_messages_list"),
    path('group/<int:id>/chat/', views.create_group_message, name="create_group_message"),
    path('group/<int:group_id>/message/<int:msg_id>/', views.create_group_like, name="create_group_like"),
]
    