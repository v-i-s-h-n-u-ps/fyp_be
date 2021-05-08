
from django.urls import path

from user.views import Login, RevokeToken, RefreshToken, SignUp, Activate, PasswordResetToken, PasswordReset, \
    PasswordChange, UserDetails, CreateStudent, ResendOTP

urlpatterns = [
    path('login/', Login.as_view(), name='login'),
    path('revoke/', RevokeToken.as_view(), name='revoke'),
    path('refresh/', RefreshToken.as_view(), name='refresh'),
    path('signup/', SignUp.as_view(), name='signup'),
    path('activate/', Activate.as_view(), name='activate'),
    path('password-reset-request/', PasswordResetToken.as_view(), name='password-reset-request'),
    path('password-reset/', PasswordReset.as_view(), name='password-reset'),
    path('password-change/', PasswordChange.as_view(), name='password-change'),
    path('me/', UserDetails.as_view(), name='me'),
    path('post-student-details/', CreateStudent.as_view(), name='post-student-details'),
    path('resend/', ResendOTP.as_view(), name='resend'),
]
