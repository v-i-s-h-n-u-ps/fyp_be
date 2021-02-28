from django.contrib import admin

from others.models import Task, ForumCategory, ForumUser, Forum

admin.site.register(Forum)
admin.site.register(ForumUser)
admin.site.register(ForumCategory)
admin.site.register(Task)

