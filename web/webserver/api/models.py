import django.utils.timezone
from django.db import models
from django.contrib.auth.models import User
from model_utils import FieldTracker

from django.db.models.signals import pre_delete
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


class ResourceType(models.Model):
    name = models.CharField(max_length=256)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    last_update = models.DateTimeField(default=django.utils.timezone.now)

    def save(self, *args, **kwargs) -> None:
        self.last_update = django.utils.timezone.now()
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
        self.storage_id.resource_count += self.resource_count
        self.storage_id.save()

    def __str__(self) -> str:
        return f'{self.storage_id.name} {'<-' if self.resource_count > 0 else '->'} {abs(self.resource_count)}'


@receiver(pre_delete, sender=Transaction)
def on_transaction_deleted(sender, instance, using, **kwargs):
    storage = ResourceStorage.objects.get(pk=instance.storage_id.pk)
    storage.resource_count -= instance.resource_count
    storage.save()


@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
