from django.urls import path
from .views import AccessPage_Role
urlpatterns = [
    path('', AccessPage_Role.as_view(), name='access-page-role'),
    path('<pk>/', AccessPage_Role.as_view(), name='access-page-role-by-id')
]
