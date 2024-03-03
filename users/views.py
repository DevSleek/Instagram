from rest_framework import permissions
from rest_framework.generics import CreateAPIView
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.exceptions import ValidationError
from django.utils.datetime_safe import datetime
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import UpdateAPIView

from .serializers import SignUpSerializer, ChangeUserInfoSerializer
from .models import User, DONE, CODE_VERIFIED, NEW, VIA_EMAIL, VIA_PHONE
from shared.utility import send_email, send_phone_code


class CreateUserAPIView(CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = SignUpSerializer


class UserVerifyAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        user = self.request.user
        code = self.request.data.get('code')

        self.check_verify(user, code)
        return Response(
            data={
                "success": True,
                "auth_status": user.auth_status,
                "access": user.token()['access'],
                "refresh": user.token()['refresh_token']
            }
        )

    @staticmethod
    def check_verify(user, code):
        verifies = user.verify_codes.filter(expiration_time__gte=datetime.now(), code=code, is_confirmed=False)

        if not verifies.exists():
            data = {
                "success": False,
                "message": "Your verification code is incorrect or out of date."
            }
            raise ValidationError(data)
        else:
            verifies.update(is_confirmed=True)

        if user.auth_status == NEW:
            user.auth_status = CODE_VERIFIED
            user.save()

        return True


class GetNewVevificationAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        user = self.request.user
        self.check_verification(user)
        if user.auth_type == VIA_EMAIL:
            code = user.create_verify_code(VIA_EMAIL)
            send_email(user.email, code)
        elif user.auth_type == VIA_PHONE:
            code = user.create_verify_code(VIA_PHONE)
            send_phone_code(user.phone_number, code)
        else:
            data = {
                'message': 'Invalid email or phone number.'
            }
            raise ValidationError(data)
        return Response(
            {
                'success': True,
                'message': 'Your verification code has been resent.'
            }
        )

    @staticmethod
    def check_verification(user):
        verifies = user.verify_codes.filter(expiration_time__gte=datetime.now(), is_confirmed=False)
        if verifies.exists():
            data = {
                'success': False,
                'messages': 'Wait a little while your code is still usable.'
            }
            raise ValidationError(data)


class ChangeUserInfoAPIView(UpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ChangeUserInfoSerializer
    http_method_names = ['patch', 'put']

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        super(ChangeUserInfoAPIView, self).update(request, *args, **kwargs)
        data = {
            'success': True,
            'message': 'User updated successfully',
            'auth_status': self.request.user.auth_status
        }
        return Response(data, status=200)

    def partial_update(self, request, *args, **kwargs):
        super(ChangeUserInfoAPIView, self).partial_update(request, *args, **kwargs)
        data = {
            'success': True,
            'message': 'User partial updated successfully',
            'auth_status': self.request.user.auth_status
        }
        return Response(data, status=200)