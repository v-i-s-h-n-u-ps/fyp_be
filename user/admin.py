from django.contrib import admin

from user.models import User, OTP

admin.site.register(User)
admin.site.register(OTP)
