import django.utils.timezone
from django.db import models
from django.contrib.auth.models import User
from model_utils import FieldTracker

from django.db.models.signals import pre_delete
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

import json


class ResourceType(models.Model):
    name = models.CharField(max_length=256)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    last_update = models.DateTimeField(default=django.utils.timezone.now)

    def save(self, *args, **kwargs) -> None:
        self.last_update = django.utils.timezone.now()
        write_change_log(str(self.user_id.pk), 'update', 'resource', django.utils.timezone.now(), {
            'pk': self.pk,
            'name': self.name
        })
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f'{self.name}'


class ResourceStorage(models.Model):
    name = models.CharField(max_length=256)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    resource_type = models.ForeignKey(ResourceType, on_delete=models.CASCADE)
    resource_count = models.FloatField(default=0)
    last_update = models.DateTimeField(default=django.utils.timezone.now)

    def save(self, *args, **kwargs) -> None:
        self.last_update = django.utils.timezone.now()
        write_change_log(str(self.user_id.pk), 'update', 'storage', django.utils.timezone.now(), {
            'pk': self.pk,
            'name': self.name,
            'resource_count': self.resource_count,
            'resource_type': self.resource_type.pk
        })
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f'{self.name}'


class Transaction(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    storage_id = models.ForeignKey(ResourceStorage, on_delete=models.CASCADE)
    resource_count = models.FloatField(default=0)
    time_stamp = models.DateTimeField(default=django.utils.timezone.now)
    tracker = FieldTracker(fields=('resource_count',))
    last_update = models.DateTimeField(default=django.utils.timezone.now)

    @tracker
    def save(self, *args, **kwargs) -> None:
        if self.pk:
            self.storage_id.resource_count -= self.tracker.previous('resource_count')
        self.last_update = django.utils.timezone.now()
        super().save(*args, **kwargs)
        write_change_log(str(self.user_id.pk), 'update', 'transaction', django.utils.timezone.now(), {
            'pk': self.pk,
            'storage_id': self.storage_id.pk,
            'resource_count': self.resource_count,
            'time_stamp': self.time_stamp.isoformat()
        })
        self.storage_id.resource_count += self.resource_count
        self.storage_id.save()

    def __str__(self) -> str:
        return f'{self.storage_id.name} {'<-' if self.resource_count > 0 else '->'} {abs(self.resource_count)}'


@receiver(pre_delete, sender=Transaction)
def on_transaction_deleted(sender, instance, using, **kwargs):
    write_change_log(str(instance.user_id.pk), 'delete', 'transaction', django.utils.timezone.now(), {
        'pk': instance.pk,
        'storage_id': instance.storage_id.pk,
        'resource_count': instance.resource_count,
        'time_stamp': instance.time_stamp.isoformat()
    })
    storage = ResourceStorage.objects.get(pk=instance.storage_id.pk)
    storage.resource_count -= instance.resource_count
    storage.save()


@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


def write_change_log(user_pk: str, operation_type: str, object_type: str, time_stamp: django.utils.timezone.datetime, operation_data: dict) -> None:
    with open('static/change_log.json', 'r') as file:
        data = json.load(file)
    data[user_pk].append({
        'operation_type': operation_type,
        'object_type': object_type,
        'time_stamp': time_stamp.isoformat(),
        'data': operation_data
    })
    with open('static/change_log.json', 'w') as file:
        json.dump(data, file, indent=2)
