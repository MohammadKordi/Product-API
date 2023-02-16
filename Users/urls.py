from django.urls import path
from . views import UserView
urlpatterns = [
    path('', UserView.as_view(), name="user"),
    path('<pk>/', UserView.as_view(), name="get_user_by_id")
]
