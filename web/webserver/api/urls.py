from django.urls import path, include

from rest_framework import routers
from rest_framework_simplejwt import views as rest_views


from . import views


router = routers.DefaultRouter()
router.register(r'resource_types', views.ResourceTypeViewSet, basename='resource_type')
router.register(r'storages', views.StorageViewSet, basename='storage')
router.register(r'transactions', views.TransactionViewSet, basename='transaction')

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('token/', rest_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', rest_views.TokenRefreshView.as_view(), name='token_refresh'),
]

urlpatterns += router.urls
