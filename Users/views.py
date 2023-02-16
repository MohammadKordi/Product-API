import re
import Roles.models
from Users.models import Users
from rest_framework import status
from .Serializer import UserSerializer
from rest_framework.views import APIView
from result_message import result_message
from rest_framework.response import Response
from django_regex.validators import RegexValidator


class UserView(APIView):
    users = Users.objects.all()

    def get(self, request, pk=None):
        if pk is None:
            message = result_message("OK", status.HTTP_200_OK, self.users.values())
            return Response(message, status=status.HTTP_200_OK)
        else:
            try:
                user = Users.objects.get(id=pk)
                message = result_message("OK", status.HTTP_200_OK, user)
                return Response(message, status=status.HTTP_200_OK)

            except Exception as ex:
                message = result_message("Not Found", status.HTTP_404_NOT_FOUND, 'Null')
                return Response(message, status=status.HTTP_200_OK)

    def post(self, request):
        try:
            UserSerializer.first_name = request.data["first_name"]
            UserSerializer.last_name = request.data["last_name"]
            UserSerializer.mobile = request.data["mobile"]
            UserSerializer.username = request.data["username"]
            UserSerializer.email = request.data["email"]
            role = ""

            # Start Check Mobile
            validate_phone_number_pattern = "^\\+?[1-9][0-9]{8,14}$"
            regex_mobile = re.match(validate_phone_number_pattern, UserSerializer.mobile)
            message = result_message("Mobile is Wrong", status.HTTP_400_BAD_REQUEST, "The Mobile input value is Wrong")
            find_mobile_in_db = Users.objects.filter(mobile=UserSerializer.mobile)

            if regex_mobile is None or find_mobile_in_db is not None:
                return Response(message, status=status.HTTP_400_BAD_REQUEST)

            return Response("OK")
            # End Check Mobile

            # Start Check Email

            # End Check Email

            # Start Role
            find_role = Roles.models.Roles.objects.filter(role_name='User')
            if not find_role:
                create_role = Roles.models.Roles.objects.create(role_name="User")
                role = create_role.id
            else:
                role = find_role[0].id
            # End Role
            user = Users.objects.create_user(
                mobile=UserSerializer.mobile,
                username=UserSerializer.username,
                role_id=role,
                email=UserSerializer.email,
                first_name=UserSerializer.first_name,
                last_name=UserSerializer.last_name
            )

            message = result_message("Create", status.HTTP_201_CREATED, user.username)
            return Response(message, status=status.HTTP_201_CREATED)

        except Exception as ex:
            message = result_message("Bad Request", status.HTTP_400_BAD_REQUEST, "Not Created")
            return Response(message, status=status.HTTP_400_BAD_REQUEST)
