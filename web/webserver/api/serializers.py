from django.contrib.auth.models import User
from rest_framework import serializers

from .models import ResourceStorage, ResourceType


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class StorageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResourceStorage
        fields = ['name', 'resource_type', 'resource_count']


class ResourceTypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ResourceType
        fields = ['name']
