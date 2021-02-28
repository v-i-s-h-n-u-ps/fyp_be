from django.contrib import admin

from projects.models import Project, ProjectCategory, ProjectParticipant, ProjectTask

admin.site.register(Project)
admin.site.register(ProjectCategory)
admin.site.register(ProjectParticipant)
admin.site.register(ProjectTask)
