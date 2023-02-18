from rest_framework import permissions
from rest_framework.response import Response

from AccessPage_Role.models import Access_Page_Role
from Access_Page.models import AccessPage


class PermissionRole(permissions.IsAdminUser):
    def has_permission(self, request, view):
        try:
            role_id = request.user.role_id
            user_permission = request.user
            find_access_page = Access_Page_Role.objects.filter(role_id=role_id)
            access_page = False

            for key in find_access_page.values():
                try:
                    access_page = bool(AccessPage.objects.get(
                        id=key['AccessPage_id'],
                        method=request.method,
                        page=request.path
                    ))
                except Exception as ex:
                    access_page = False
                    print(ex)
        except Exception as ex:
            access_page = False

        if request.method == "GET" and access_page:
            return request.method == 'Get' or user_permission

        if request.method == "POST" and access_page:
            return request.method == 'POST' or user_permission

        if request.method == "Put" and access_page:
            return request.method == 'Put' or user_permission

        if request.method == "Delete" and access_page:
            return request.method == 'Delete' or user_permission
