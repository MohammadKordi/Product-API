from rest_framework import status
from rest_framework.views import APIView
from result_message import result_message
from Access_Page.models import AccessPage
from rest_framework.response import Response
from Access_Page.Serializer import Serializer


class AccessPageView(APIView):

    def get(self, request, pk=None):
        if pk is None:
            access_page = AccessPage.objects.all().values()
            message = result_message(
                'ok',
                status.HTTP_200_OK,
                access_page
            )
            return Response(message)
        else:
            try:
                access_page = AccessPage.objects.get(id=pk)
                message = result_message(
                    'ok',
                    status.HTTP_200_OK,
                    access_page
                )
                return Response(message)
            except Exception as ex:
                message = result_message(
                    "Bad Request",
                    status.HTTP_400_BAD_REQUEST,
                    ""
                )
                return Response(message, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        find_request_page = bool('page' in request.data)
        find_request_method = bool('method' in request.data)
        if not find_request_page:
            message = result_message(
                'The input Values Should be the Same as the Result',
                status.HTTP_400_BAD_REQUEST,
                {
                    "page": "page",
                    "method": "method"
                }
            )
            return Response(message, status=status.HTTP_400_BAD_REQUEST)

        if not find_request_method:
            message = result_message(
                'The input values should be the same as the Result',
                status.HTTP_400_BAD_REQUEST,
                {
                    "page": "page",
                    "method": "method"
                }
            )
            return Response(message, status=status.HTTP_400_BAD_REQUEST)
        Serializer.page = request.data['page']
        Serializer.method = request.data['method']

        access_page = AccessPage.objects.create(
            page=Serializer.page,
            method=Serializer.method
        )
        message = result_message(
            "ok",
            status.HTTP_200_OK,
            {
                "page": access_page.page,
                "method": access_page.method,
            }
        )

        return Response(message, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        try:
            access_page = AccessPage.objects.get(id=pk)
            access_page.delete()
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
