from django.contrib import admin
from .models import ResourceType, ResourceStorage, Transaction


class ResourceAdmin(admin.ModelAdmin):
    list_display = ('name', 'user_id')


class ResourceStorageAdmin(admin.ModelAdmin):
    list_display = ('name', 'user_id', 'resource_type', 'resource_count')


admin.site.register(ResourceType, ResourceAdmin)
admin.site.register(ResourceStorage, ResourceStorageAdmin)
admin.site.register(Transaction)
