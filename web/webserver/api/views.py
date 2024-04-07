from django.http import HttpResponse
from django.contrib.auth.models import User

from .serializers import UserSerializer

from rest_framework import permissions, viewsets
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import IsAuthenticated, IsAdminUser


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


@permission_classes((IsAuthenticated, IsAdminUser))
@api_view(['GET'])
def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")
