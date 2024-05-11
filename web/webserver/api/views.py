from django.http import HttpResponse
from django.contrib.auth.models import User

from rest_framework import permissions, viewsets, generics, status, views
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

import json

from .models import ResourceStorage, ResourceType, Transaction
from .serializers import UserSerializer, StorageSerializer, ResourceTypeSerializer, TransactionSerializer


class PingView(views.APIView):
    def get(self, request, format=None) -> Response:
        data = {
            'status': 'ok',
        }
        return Response(data)


class ChangeLog(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None) -> Response:
        with open('static/change_log.json', 'r') as file:
            data = json.load(file)
            return Response(data[str(request.user.pk)])


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class StorageViewSet(generics.ListCreateAPIView):
    serializer_class = StorageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ResourceStorage.objects.filter(user_id=self.request.user.pk)


class StorageDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = StorageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ResourceStorage.objects.filter(user_id=self.request.user.pk)


class ResourceTypeViewSet(generics.ListCreateAPIView):
    serializer_class = ResourceTypeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ResourceType.objects.filter(user_id=self.request.user.pk)


class ResourceTypeDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ResourceTypeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ResourceType.objects.filter(user_id=self.request.user.pk)


class TransactionViewSet(generics.ListCreateAPIView):
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]
    ordering = ('-time_stamp')

    def get_queryset(self):
        return Transaction.objects.filter(user_id=self.request.user.pk)

    def post(self, request, *args, **kwargs):
        temp = request.data.copy()
        temp['user_id'] = request.user.pk
        serializer = self.serializer_class(data=temp)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class TransactionDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Transaction.objects.filter(user_id=self.request.user.pk)
