from django.urls import path

from others.views import CreateTask, CreateForum, GetForum, GetForumsUserIsPartOf, UpdateUsersOfForum, UpdateForum

urlpatterns = [
    path('task/', CreateTask.as_view(), name='task'),
    path('create-forum/', CreateForum.as_view(), name='create-forum'),
    path('get-forum/', GetForum.as_view(), name='get-forum'),
    path('get-forums/', GetForumsUserIsPartOf.as_view(), name='get-user-forums'),
    path('manage-forum-users/', UpdateUsersOfForum.as_view(), name='manage-forum-users'),
    path('update-forums/', UpdateForum.as_view(), name='update-forum'),
]