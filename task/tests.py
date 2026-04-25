from django.test import TestCase
from accounts.models import User
from task.serialezers import ProjectCreateSerializer


class ProjectCreateSerializerTest(TestCase):
    def setUp(self):
        data_valid = {
            'title': 'test',
            'content': 'test',
        }

        self.serializer = ProjectCreateSerializer(data=data_valid)

    def test_registration_valid(self):
        self.assertTrue(self.serializer.is_valid())

