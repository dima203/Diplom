from django.test import TestCase
from api.models import ResourceType, User


class TestResourceType(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create(username='Tester')
        ResourceType.objects.create(name='test', user_id=self.user)

    def test_resource_type_creation(self) -> None:
        self.assertIsNotNone(ResourceType.objects.get(user_id=self.user))
