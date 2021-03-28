from django.urls import path

from others.views import CreateTask

urlpatterns = [
    path('task/', CreateTask.as_view(), name='task')
]