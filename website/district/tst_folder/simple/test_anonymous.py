from django.contrib.auth.models import AnonymousUser
from django.test import TransactionTestCase, RequestFactory
from django.urls import reverse

from config.constants.route_cnf import PAGES


class AnonymousTest(TransactionTestCase):

    def __init__(self, methodName='test_all'):
        print(f"\33[38;2;0;255;0m INIT {methodName}\33[0m")
        super().__init__(methodName)

    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()

    # it doesn't work, it seems we'll have to write a test for each routes
    # python manage.py test district.tst_folder.simple.test_anonymous
    def test_anonymous_user_access(self):
        for page in PAGES:
            with self.subTest():
                arguments = []
                if page.name == 'activate':
                    arguments = ["12", "121"]
                request = self.factory.get(reverse(page.name, args=arguments))
                request.user = AnonymousUser()
                response = page.ctrl(request)
                if page.type == "view":
                    if page.log_req:
                        self.assertEqual(response.status_code, 302)
                    else:
                        self.assertEqual(response.status_code, 200)
