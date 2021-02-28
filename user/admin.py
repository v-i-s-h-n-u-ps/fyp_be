from django.contrib import admin

from user.models import User, OTP, Student, StudentCategory, UserRole

admin.site.register(User)
admin.site.register(UserRole)
admin.site.register(OTP)
admin.site.register(Student)
admin.site.register(StudentCategory)
