import json

from django.contrib.auth.models import AnonymousUser
from django.core import management
from django.test import TransactionTestCase, RequestFactory, Client

from district.models.group import GroupDC
from district.models.user import UserDC
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

    # TODO : not working
    def test_json_group_register(self):
        page = PageManager().get_page('group_register')
        for user in UserDC.objects.filter(id__gt=0).all():
            for group in GroupDC.objects.all():
                request = self.factory.post(page.url, {"register_key": group.register_key})
                request.user = user
                response = page.ctrl(request)
                dict_json = json.loads(response.content)
                print(f"[user: {user.username}][group: {group.id}]")
                print("groups:", GroupDC.objects.filter(id=group.id, userdc=user.id).all())
                # district.GroupDC.None -> not a group but counted as one
                if len(GroupDC.objects.filter(id=group.id, userdc=user.id).all()) != 0:
                    with self.subTest():
                        self.assertEqual(dict_json["exit_code"], 9)
                    with self.subTest():
                        self.assertIn("err_msg", dict_json)
                else:
                    with self.subTest():
                        self.assertEqual(dict_json["exit_code"], 0)
                    with self.subTest():
                        self.assertNotIn("err_msg", dict_json)

            # test empty key
            request = self.factory.post(page.url, {"register_key": ""})
            request.user = user
            response = page.ctrl(request)
            dict_json = json.loads(response.content)
            with self.subTest():
                self.assertEqual(dict_json["exit_code"], 2)
            with self.subTest():
                self.assertIn("err_msg", dict_json)

            # test key which doesn't exist
            request = self.factory.post(page.url, {"register_key": "Tu lis mon code ? Bonne chance"})
            request.user = user
            response = page.ctrl(request)
            dict_json = json.loads(response.content)
            with self.subTest():
                self.assertEqual(dict_json["exit_code"], 1)
            with self.subTest():
                self.assertIn("err_msg", dict_json)
