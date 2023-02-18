from rest_framework import status

from Permissions import PermissionRole
from .Serializers import Serializer
from .models import Access_Page_Role
from rest_framework.views import APIView
from result_message import result_message
from rest_framework.response import Response


class AccessPage_Role(APIView):
    permission_classes = [PermissionRole]

    def get(self, request, pk=None):
        try:
            if pk is None:
                result = Access_Page_Role.objects.all()
                message = result_message(
                    'ok',
                    status.HTTP_200_OK,
                    result.values()
                )
                return Response(message, status=status.HTTP_200_OK)
            else:
                result = Access_Page_Role.objects.get(id=pk)
                message = result_message(
                    'ok',
                    status.HTTP_200_OK,
                    result
                )
                return Response(message, status=status.HTTP_200_OK)
        except Exception as ex:
            message = result_message(
                'Error',
                status.HTTP_400_BAD_REQUEST,
                ''
            )
            return Response(message, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        try:
            find_request_role = bool('role' in request.data)
            if not find_request_role:
                message = result_message(
                    'The input Values Should be the Same as the Result',
                    status.HTTP_400_BAD_REQUEST,
                    {
                        "role": "role_id",
                        "accessPage": "accessPage_id"
                    }
                )
                return Response(message, status=status.HTTP_400_BAD_REQUEST)

            find_request_accessPage = bool('accessPage' in request.data)
            if not find_request_accessPage:
                message = result_message(
                    'The input Values Should be the Same as the Result',
                    status.HTTP_400_BAD_REQUEST,
                    {
                        "role": "role_id",
                        "accessPage": "accessPage_id"
                    }
                )
                return Response(message, status=status.HTTP_400_BAD_REQUEST)
            Serializer.role = request.data['role']
            Serializer.accessPage = request.data['accessPage']
            Access_Page_Role.objects.create(
                role_id=Serializer.role,
                AccessPage_id=Serializer.accessPage
            )

            message = result_message(
                'OK',
                status.HTTP_201_CREATED,
                'Create'
            )
            return Response(message)

        except Exception as ex:
            message = result_message(
                'Error',
                status.HTTP_400_BAD_REQUEST,
                ''
            )
            return Response(message, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            Access_Page_Role.objects.get(id=pk).delete()
            message = result_message(
                'ok',
                status.HTTP_204_NO_CONTENT,
                'Delete'
            )

            return Response(message, status=status.HTTP_204_NO_CONTENT)

        except Exception as ex:
            message = result_message(
                'Error',
                status.HTTP_400_BAD_REQUEST,
                ''
            )

            return Response(message, status=status.HTTP_400_BAD_REQUEST)
