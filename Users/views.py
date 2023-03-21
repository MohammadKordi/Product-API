import re
import Roles.models
from Users.models import Users
from rest_framework import status
from Permissions import PermissionRole
from .Serializer import UserSerializer
from rest_framework.views import APIView
from result_message import result_message
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework.authtoken.models import Token


class UserView(APIView):
    users = Users.objects.all()

    # permission_classes = [PermissionRole]

    def get(self, request, pk=None):
        if pk is None:
            userList = []
            for user in self.users:
                if user.is_deleted == False:
                    if user.role:
                        userObject = {
                            'id': user.id,
                            'first_name': user.first_name,
                            'last_name': user.last_name,
                            'mobile': user.mobile,
                            'email': user.email,
                            'username': user.username,
                            'role': user.role.role_name,
                            'registered': user.date_joined,
                        }
                    else:
                        userObject = {
                            'id': user.id,
                            'first_name': user.first_name,
                            'last_name': user.last_name,
                            'mobile': user.mobile,
                            'email': user.email,
                            'username': user.username,
                            'role': null,
                            'registered': user.date_joined,
                        }
                    userList.extend([userObject])
            message = result_message("OK", status.HTTP_200_OK, userList)
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
            UserSerializer.password = request.data["password"]
            role = ""

            # Start Check Mobile
            validate_phone_number_pattern = "^\\+?[1-9][0-9]{9,14}$"
            regex_mobile = bool(re.match(validate_phone_number_pattern, UserSerializer.mobile))
            find_mobile_in_db = bool(Users.objects.filter(mobile=UserSerializer.mobile))

            message_mobile_regex = result_message(
                "Mobile is Wrong",
                status.HTTP_400_BAD_REQUEST,
                "The Mobile input value is Wrong"
            )

            message_mobile_find = result_message(
                "Duplicate Mobile",
                status.HTTP_400_BAD_REQUEST,
                "The Mobile is Duplicate"
            )

            if find_mobile_in_db is True:
                return Response(message_mobile_find, status=status.HTTP_400_BAD_REQUEST)

            if regex_mobile is False:
                return Response(message_mobile_regex, status=status.HTTP_400_BAD_REQUEST)

            # return Response("OK")
            # End Check Mobile

            # Start Check Email
            validate_email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
            find_email_in_db = bool(Users.objects.filter(email=UserSerializer.email))
            regex_email = bool(re.fullmatch(validate_email_pattern, UserSerializer.email))
            message_email_regex = result_message(
                "Email is Wrong",
                status.HTTP_400_BAD_REQUEST,
                "The Email input value is Wrong"
            )

            message_email_find = result_message(
                "Duplicate Email",
                status.HTTP_400_BAD_REQUEST,
                "The Email is Duplicate"
            )

            if find_email_in_db is True:
                return Response(message_email_find, status=status.HTTP_400_BAD_REQUEST)

            if regex_email is False:
                return Response(message_email_regex, status=status.HTTP_400_BAD_REQUEST)

            # End Check Email

            # Start UserName
            find_username_in_db = bool(Users.objects.filter(username=UserSerializer.username))

            message_username_find = result_message(
                "Duplicate UserName",
                status.HTTP_400_BAD_REQUEST,
                "The UserName is Duplicate"
            )
            if find_username_in_db is True:
                return Response(message_username_find, status=status.HTTP_400_BAD_REQUEST)

            # End UserName

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
                last_name=UserSerializer.last_name,
                password=UserSerializer.password,
            )

            Token.objects.create(user=user)
            message = result_message("Create", status.HTTP_201_CREATED, user.username)
            return Response(message, status=status.HTTP_201_CREATED)

        except Exception as ex:
            message = result_message("Bad Request", status.HTTP_400_BAD_REQUEST, "Not Created")
            return Response(message, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            user = Users.objects.get(id=pk)
            user.is_deleted = true
            user.save()
            message = result_message(
                "Delete",
                status.HTTP_204_NO_CONTENT,
                "The Deletion was Successful"
            )
            return Response(message)

        except Exception as ex:
            message = result_message(
                "Failed",
                status.HTTP_400_BAD_REQUEST,
                "The Delete operation was not Successful"
            )
            return Response(message)


class Login(APIView):
    def post(self, request):
        # start Check UserName
        find_request_username = bool('username' in request.data)
        message_username = result_message("Bad Request", status.HTTP_400_BAD_REQUEST, "Request username does not exist")
        if find_request_username is False:
            return Response(message_username, status=status.HTTP_400_BAD_REQUEST)
        # End Check UserName

        # start Check Password
        find_request_password = bool('password' in request.data)
        message_password = result_message("Bad Request", status.HTTP_400_BAD_REQUEST, "Request password does not exist")
        if find_request_password is False:
            return Response(message_password, status=status.HTTP_400_BAD_REQUEST)
        # End Check Password

        username = request.data['username']
        password = request.data['password']

        user = authenticate(username=username, password=password)

        if user is not None:
            message = result_message(
                "Token",
                status.HTTP_200_OK,
                user.auth_token.key
            )
            return Response(message, status=status.HTTP_200_OK)
        else:
            message_bad_request = result_message(
                "UNAUTHORIZED",
                status.HTTP_401_UNAUTHORIZED,
                ""
            )
            return Response(message_bad_request, status=status.HTTP_401_UNAUTHORIZED)


class ChangeRoleUser(APIView):
    def post(self, request, pk):
        try:
            user = Users.objects.get(id=pk)
            role = Roles.models.Roles.objects.get(id=request.data['roleId'])
            print(role.id)
            user.role_id = role.id
            user.save()
            message = result_message(
                "Change Role",
                status.HTTP_200_OK,
                {"role ": user.role.role_name, 'user': user.username}
            )
            return Response(message, status=status.HTTP_200_OK)
        except Exception as e:
            message_bad_request = result_message(
                "Not Found User or Role",
                status.HTTP_400_BAD_REQUEST,
                request.data['roleId']
            )
            return Response(message_bad_request, status=status.HTTP_400_BAD_REQUEST)
