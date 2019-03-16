from django.test import TestCase
from db.models import  User


class TestModels(TestCase):

    def test_teest(self):
        user = User(name="matt")
        self.assertEqual(user.name, "matt")
