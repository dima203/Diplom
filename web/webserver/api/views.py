from django.http import HttpResponse
from django.contrib.auth.models import User

from rest_framework import permissions, viewsets
from rest_framework_simplejwt.tokens import AccessToken

from .models import ResourceStorage, ResourceType, Transaction
from .serializers import UserSerializer, StorageSerializer, ResourceTypeSerializer, TransactionSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class StorageViewSet(viewsets.ModelViewSet):
    serializer_class = StorageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ResourceStorage.objects.filter(user_id=self.request.user.pk)


class ResourceTypeViewSet(viewsets.ModelViewSet):
    serializer_class = ResourceTypeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ResourceType.objects.filter(user_id=self.request.user.pk)


class TransactionViewSet(viewsets.ModelViewSet):
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Transaction.objects.filter(user_id=self.request.user.pk)
