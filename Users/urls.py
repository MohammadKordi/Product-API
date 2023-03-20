from django.urls import path
from .views import UserView, Login, ChangeRoleUser

urlpatterns = [
    path('', UserView.as_view(), name="user"),
    path("login/", Login.as_view(), name="login"),
    path('<pk>/', UserView.as_view(), name="get_user_by_id"),
    path('changerole/<pk>/', ChangeRoleUser.as_view(), name="change_role_user"),
]
