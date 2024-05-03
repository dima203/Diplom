from django.contrib.auth.models import User
from rest_framework import serializers

from .models import ResourceStorage, ResourceType, Transaction


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class StorageSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        return ResourceStorage.objects.create(**validated_data)

    class Meta:
        model = ResourceStorage
        fields = ['pk', 'user_id', 'name', 'resource_type', 'resource_count', 'last_update']


class ResourceTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResourceType
        fields = ['pk', 'user_id', 'name', 'last_update']


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['pk', 'user_id', 'storage_id', 'resource_count', 'time_stamp', 'last_update']
