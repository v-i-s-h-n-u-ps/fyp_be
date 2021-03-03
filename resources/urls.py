
from django.urls import path

from resources.views import GetUniversity

urlpatterns = [
    path('get-university/', GetUniversity.as_view(), name='get-university'),
]
