from .models import Roles
from rest_framework import status
from rest_framework.views import APIView
from .serializer import Roles_Serializers
from rest_framework.response import Response


# Create your views here.


class RoleView(APIView):
    roles = Roles.objects.all()

    def result_message(self, message, status_code, result):
        message = {
            "message": message,
            'status_code': status_code,
            'result': result
        }
        return message

    def get(self, request, pk=None):
        if pk is None:
            message = self.result_message("Ok", 200, self.roles.values())
            return Response(message, status=status.HTTP_200_OK)
        else:
            role = Roles.objects.filter(id=pk).values()
            if not role:
                message = self.result_message("Not Found", status.HTTP_404_NOT_FOUND, 'null')
                return Response(message, status=status.HTTP_404_NOT_FOUND)
            else:
                message = self.result_message("Ok", status.HTTP_200_OK, role)
                return Response(message, status=status.HTTP_200_OK)

    def post(self, request):
        find_role = Roles.objects.filter(role_name=request.data['roleName'])
        if not find_role:
            Roles_Serializers.role_name = request.data['roleName']
            Roles.objects.create(role_name=Roles_Serializers.role_name)
            return Response('Create')
        else:
            return Response('The Name Already Exists')

    def put(self, request, pk):
        find_role = Roles.objects.filter(role_name=request.data['roleName'])
        if not find_role:
            try:
                role = Roles.objects.get(id=pk)
                Roles_Serializers.role_name = request.data['roleName']
                role.role_name = Roles_Serializers.role_name
                role.save()
                return Response(f'Update')
            except Exception as ex:
                return Response(f'Bad Request', status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response('The Name Already Exists')

    # def delete(self, request, pk):
