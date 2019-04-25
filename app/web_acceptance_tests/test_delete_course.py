from django.test import TestCase, Client
from app.models.account import Account


class TestDeleteCourse(TestCase):

    def setUp(self):
        self.current_user = Account.objects.create(username="the_user", password="p", name="n", is_logged_in=True,
                                                   roles=0x8)

        self.client = Client()
        self.session = self.client.session
        self.session['username'] = 'the_user'
        self.session.save()

    def test_delete_course_happy_path(self):
        self.fail()
