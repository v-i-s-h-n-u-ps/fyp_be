
from django.urls import path

from user.views import *

urlpatterns = [
    path('login/', Login.as_view(), name='login'),
    path('revoke/', RevokeToken.as_view(), name='revoke'),
    path('refresh/', RefreshToken.as_view(), name='refresh'),
    path('signup/', SignUp.as_view(), name='signup'),
]
