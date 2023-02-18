from django.urls import path
from Access_Page.views import AccessPageView

urlpatterns = [
    path("", AccessPageView.as_view(), name="access_page_view"),
    path("<pk>/", AccessPageView.as_view(), name="access_page_view_by_id")
]
