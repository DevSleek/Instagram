from shared.utility import check_email_or_phone, check_user_type, send_email, send_phone_code
from .models import User, UserConfirmation, VIA_PHONE, VIA_EMAIL, CODE_VERIFIED, DONE, PHOTO_DONE, NEW

from rest_framework import exceptions
from django.db.models import Q
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from django.core.validators import FileExtensionValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.generics import get_object_or_404
from django.contrib.auth.models import update_last_login


class SignUpSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)

    def __init__(self, *args, **kwargs):
        super(SignUpSerializer, self).__init__(*args, **kwargs)
        self.fields['email_phone_number'] = serializers.CharField(required=False)

    class Meta:
        model = User
        fields = (
            'id',
            'auth_type',
            'auth_status'
        )
        extra_kwargs = {
            'auth_type': {'read_only': True, 'required': False},
            'auth_status': {'read_only': True, 'required': False}
        }

    def create(self, validated_data):
        user = super(SignUpSerializer, self).create(validated_data)
        if user.auth_type == VIA_EMAIL:
            code = user.create_verify_code(VIA_EMAIL)
            send_email(user.email, code)
        elif user.auth_type == VIA_PHONE:
            code = user.create_verify_code(VIA_PHONE)
            send_phone_code(user.phone_number, code)
        user.save()
        return user

    def validate(self, data):
        super(SignUpSerializer, self).validate(data)
        data = self.auth_validate(data)
        return data

    @staticmethod
    def auth_validate(data):
        user_input = str(data.get('email_phone_number')).lower()
        input_type = check_email_or_phone(user_input)
        if input_type == "email":
            data = {
                "email": user_input,
                "auth_type": VIA_EMAIL
            }
        elif input_type == "phone":
            data = {
                "phone_number": user_input,
                "auth_type": VIA_PHONE
            }
        else:
            data = {
                'message': 'You must send email or phone number'
            }
            raise ValidationError(data)

        return data

    @staticmethod
    def validate_email_phone_number(value):
        value = value.lower()
        if value and User.objects.filter(email=value).exists():
            data = {
                'message': 'This email is already in use'
            }
            raise ValidationError(data)
        elif value and User.objects.filter(phone_number=value).exists():
            data = {
                'message': 'This phone number is already in use'
            }
            raise ValidationError(data)

        return value

    def to_representation(self, instance):
        data = super(SignUpSerializer, self).to_representation(instance)
        data.update(instance.token())

        return data


class ChangeUserInfoSerializer(serializers.Serializer):
    first_name = serializers.CharField(write_only=True, required=True)
    last_name = serializers.CharField(write_only=True, required=True)
    username = serializers.CharField(write_only=True, required=True)
    password = serializers.CharField(write_only=True, required=True)
    confirm_password = serializers.CharField(write_only=True, required=True)

    def validate(self, data):
        password = data.get('password')
        confirm_password = data.get('confirm_password')
        if password != confirm_password:
            raise ValidationError(
                {
                    'message': 'The passwords do not match'
                }
            )
        if password:
            validate_password(password)
            validate_password(confirm_password)
        return data

    def validate_username(self, username):
        if len(username) < 6 or len(username) > 15:
            raise ValidationError(
                {
                    'message': 'Username must be between 6 and 15 characters long'
                }
            )
        if username.isdigit():
            raise ValidationError(
                {
                    'message': 'The username is entirely numeric'
                }
            )
        return username

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.username = validated_data.get('username', instance.username)
        instance.password = validated_data.get('password', instance.password)
        if validated_data.get('password'):
            instance.set_password(validated_data.get('password'))
        if instance.auth_status == CODE_VERIFIED:
            instance.auth_status = DONE
        instance.save()
        return instance


class ChangeUserPhotoSerializer(serializers.Serializer):
    photo = serializers.ImageField(validators=[FileExtensionValidator(allowed_extensions=('jpg', 'jpeg', 'png', 'heir', 'heif'))])

    def update(self, instance, validated_data):
        photo = validated_data.get('photo')
        if photo:
            instance.photo = photo
            instance.auth_status = PHOTO_DONE
            instance.save()
        return instance


class UserLoginSerializer(TokenObtainPairSerializer):
    def __init__(self, *args, **kwargs):
        super(UserLoginSerializer, self).__init__(*args, **kwargs)
        self.fields['user_input'] = serializers.CharField(required=True)
        self.fields['username'] = serializers.CharField(read_only=True, required=False)

    def auth_validate(self, data):
        user_input = data.get('user_input')
        if check_user_type(user_input) == 'username':
            username = user_input
        elif check_user_type(user_inpu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t) == 'phone':
            user = self.get_user(phone_number=user_input)
            username = user.username
        elif check_user_type(user_input) == 'email':
            user = self.get_user(email__exact=user_input)
            username = user.username
        else:
            data = {
                'message': 'You must send an email, username or phone number'
            }
            raise ValidationError(data)
        authentication_kwargs = {
            self.username_field: username,
            'password': data['password']
        }
        current_user = User.objects.filter(username__exact=username).first()
        if current_user is not None and current_user.auth_status in [NEW, CODE_VERIFIED]:
            raise ValidationError(
                {
                    'success': False,
                    'message': 'You are not fully registered yet'
                }
            )
        user = authenticate(**authentication_kwargs)
        if user is not None:
            self.user = user
        else:
            raise ValidationError(
                {
                    'success': False,
                    'message': 'Sorry, login or password you entered is incorrect. Please check and try again!'
                }
            )

    def validate(self, attrs):
        self.auth_validate(attrs)
        if self.user.auth_status not in [DONE, PHOTO_DONE]:
            raise PermissionDenied("You can't login, you don't have permission")
        attrs = self.user.token()
        attrs['auth_status'] = self.user.auth_status
        attrs['fullname'] = self.user.full_name
        return attrs

    def get_user(self, **kwargs):
        users = User.objects.filter(**kwargs)
        if not users.exists():
            raise ValidationError(
                {
                    'message': 'No active account found'
                }
            )
        return users.first()


class LoginRefreshTokenSerializer(TokenRefreshSerializer):

    def validate(self, attrs):
        data = super().validate(attrs)
        access_token_instance = AccessToken(data['access'])
        user_id = access_token_instance['user_id']
        user = get_object_or_404(User, id=user_id)
        update_last_login(None, user)
        return data


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()


class ForgotPasswordSerializer(serializers.Serializer):
    email_or_phone = serializers.CharField(write_only=True, required=True)

    def validate(self, attrs):
         email_or_phone = attrs.get('email_or_phone')
         if email_or_phone is None:
             raise ValidationError(
                 {
                     'success': False,
                     'message': 'Email or phone number must be entered!'
                 }
             )
         user = User.objects.filter(Q(phone_number=email_or_phone) | Q(email=email_or_phone))
         if not user.exists():
             raise NotFound(detail='User not found')
         attrs['user'] = user.first()
         return attrs