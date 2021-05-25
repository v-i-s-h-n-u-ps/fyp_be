
from django.urls import path

from projects.views import CreateProject, GetProject, GetProjectParticipants, UpdateProject, GetMyProjects, \
    ListProjects, ManageProjectParticipant, AddProjectTask, GetProjectTask, UpdateProjectTask, GetFilteredProjects

urlpatterns = [
    path('create-projects/', CreateProject.as_view(), name='create-project'),
    path('get-project-details/', GetProject.as_view(), name='get-project-details'),
    path('get-project-participants/', GetProjectParticipants.as_view(), name='get-project-participants'),
    path('update-project/', UpdateProject.as_view(), name='update-project'),
    path('get-my-projects/', GetMyProjects.as_view(), name='get-my-projects'),
    path('filter-projects/', GetFilteredProjects.as_view(), name='filter-projects'),
    path('list-projects/', ListProjects.as_view(), name='list-projects'),
    path('manage-project-users/', ManageProjectParticipant.as_view(), name='manage-project-users'),
    path('add-project-task/', AddProjectTask.as_view(), name='add-project-task'),
    path('update-project-tasks/', UpdateProjectTask.as_view(), name='update-project-tasks'),
    path('get-project-task/', GetProjectTask.as_view(), name='get-project-task'),
]
