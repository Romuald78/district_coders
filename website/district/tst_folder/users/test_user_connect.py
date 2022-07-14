import random
import string

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

    def __login(self, username, password):
        url = "/accounts/login/"
        response = self.client.post(url, data={
            "username" : username,
            "password" : password,
        })
        return response

    def __randomLogin(self):
        msg1 = "Please enter a correct username and password."
        msg2 = "Note that both fields may be case-sensitive."
        username = ''.join(random.choice(string.ascii_lowercase) for i in range(8))
        password = ''.join(random.choice(string.ascii_lowercase) for i in range(8))
        response = self.__login(username, password)
        self.assertContains(response, msg1)
        self.assertContains(response, msg2)

    def __adminLogin(self):
        response = self.__login("admin", "admin")
        self.assertRedirects(response, PageManager().get_URL("profile"))

    def test_user_connect(self):
        # Check random user name and password
        self.__randomLogin()
        # Check admin user
        self.__adminLogin()
