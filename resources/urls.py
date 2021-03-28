
from django.urls import path

from resources.views import GetUniversity, GetRole, GetType, GetCategory

urlpatterns = [
    path('get-university/', GetUniversity.as_view(), name='get-university'),
    path('get-role/', GetRole.as_view(), name='get-role'),
    path('get-types/', GetType.as_view(), name='get-types'),
    path('get-category/', GetCategory.as_view(), name='get-category'),
]