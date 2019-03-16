from django.test import TestCase
from app.models.user_model import User


class TestModels(TestCase):

    def test_test(self):
        user = User(name="matt")
        self.assertEqual(user.name, "matt")
