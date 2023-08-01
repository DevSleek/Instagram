from rest_framework import permissions
from rest_framework.generics import CreateAPIView
from rest_framework.decorators import permission_classes

from .serializers import SignUpSerializer
from .models import User


class CreateUserView(CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny, )
    serializer_class = SignUpSerializer


