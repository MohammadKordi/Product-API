from django.urls import path
from .views import UserView, Login

urlpatterns = [
    path('', UserView.as_view(), name="user"),
    path("login/", Login.as_view(), name="login"),
    path('<pk>/', UserView.as_view(), name="get_user_by_id"),
]
