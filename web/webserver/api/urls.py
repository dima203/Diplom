from django.urls import path, include

from rest_framework_simplejwt import views as rest_views


from . import views


urlpatterns = [
    path(r'resource_types', views.ResourceTypeViewSet.as_view(), name='resource_type'),
    path(r'resource_types/<int:pk>', views.ResourceTypeDetail.as_view(), name='resource_type_detail'),
    path(r'storages', views.StorageViewSet.as_view(), name='storage'),
    path(r'storages/<int:pk>/', views.StorageDetail.as_view(), name='storage_detail'),
    path(r'transactions', views.TransactionViewSet.as_view(), name='transaction'),
    path(r'transactions/<int:pk>', views.TransactionDetail.as_view(), name='transaction_detail'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('token/', rest_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', rest_views.TokenRefreshView.as_view(), name='token_refresh'),
]
