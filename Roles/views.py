from Permissions import PermissionRole
from .models import Roles
from rest_framework import status
from rest_framework.views import APIView
from result_message import result_message
from .serializer import Roles_Serializers
from rest_framework.response import Response


class RoleView(APIView):
    permission_classes = [PermissionRole]
    roles = Roles.objects.all()

    def get(self, request, pk=None):
        if pk is None:
            message = result_message("Ok", 200, self.roles.values())
            return Response(message, status=status.HTTP_200_OK)
        else:
            role = Roles.objects.filter(id=pk).values()
            if not role:
                message = result_message("Not Found", status.HTTP_404_NOT_FOUND, 'null')
                return Response(message, status=status.HTTP_404_NOT_FOUND)
            else:
                message = result_message("Ok", status.HTTP_200_OK, role)
                return Response(message, status=status.HTTP_200_OK)

    def post(self, request):
        find_role = Roles.objects.filter(role_name=request.data['roleName'])
        if not find_role:
            Roles_Serializers.role_name = request.data['roleName']
            Roles.objects.create(role_name=Roles_Serializers.role_name)
            message = result_message("Ok", status.HTTP_201_CREATED, 'Create')
            return Response(message, status=status.HTTP_201_CREATED)
        else:
            message = result_message("The Name Already Exists", status.HTTP_400_BAD_REQUEST, 'Not Created')
            return Response(message, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        find_role = Roles.objects.filter(role_name=request.data['roleName'])
        if not find_role:
            try:
                role = Roles.objects.get(id=pk)
                Roles_Serializers.role_name = request.data['roleName']
                role.role_name = Roles_Serializers.role_name
                role.save()
                message = result_message("Update", status.HTTP_200_OK, 'Update')
                return Response(message, status=status.HTTP_200_OK)
            except Exception as ex:
                message = result_message("Not Found", status.HTTP_404_NOT_FOUND, 'Not Updated')
                return Response(message, status=status.HTTP_400_BAD_REQUEST)
        else:
            message = result_message("The Name Already Exists", status.HTTP_400_BAD_REQUEST, 'Not Updated')
            return Response(message, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            role = Roles.objects.get(id=pk)
            role.delete()
            message = result_message("Delete", status.HTTP_204_NO_CONTENT, 'Delete')
            return Response(message, status=status.HTTP_204_NO_CONTENT)
        except Exception as ex:
            message = result_message("Not Found", status.HTTP_404_NOT_FOUND, 'Not Found')
            return Response(message, status=status.HTTP_404_NOT_FOUND)
