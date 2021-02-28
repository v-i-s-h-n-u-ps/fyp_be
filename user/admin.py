from django.contrib import admin

from user.models import User, OTP, StudentDetails, StudentCategory

admin.site.register(User)
admin.site.register(OTP)
admin.site.register(StudentDetails)
admin.site.register(StudentCategory)
