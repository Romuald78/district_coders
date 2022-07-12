from django.core import management
from django.test import TransactionTestCase, RequestFactory, Client

from toolbox.utils.route_mgr import PageManager


class UserConnectTest(TransactionTestCase):

    def __init__(self, methodName=''):
        print(f"\33[38;2;0;255;0m USER CONNECT {methodName}\33[0m")
        super().__init__(methodName)

    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()
        self.client  = Client()
        management.call_command("dc_reinit")
        management.call_command("populate_multi")

    def test_user_connect(self):
        url = "/accounts/login/"
        response = self.client.post(url, data={
            "username" : "admin",
            "password" : "admin",
        })
        # If connection ok, redirect to profile page
        self.assertRedirects(response, PageManager().get_URL("profile"))

