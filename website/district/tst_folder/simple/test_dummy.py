from django.contrib.auth.models import AnonymousUser
from django.test import SimpleTestCase, RequestFactory

from district.controllers.ctrl_user import ctrl_user_profile


class SimpleTest(SimpleTestCase):
    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()

    def test1(self):
        request = self.factory.get("/accounts/profile")
        request.user = AnonymousUser()
        response = ctrl_user_profile(request)
        self.assertEqual(response.status_code, 302)

    def test2(self):
        pass
