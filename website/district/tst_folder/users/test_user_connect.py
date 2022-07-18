import os
import random
import string
import json

from django.contrib.auth.models import AnonymousUser
from django.core import management
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TransactionTestCase, RequestFactory, Client

from district.models.group import GroupDC
from district.models.user import UserDC
from toolbox.utils.route_mgr import PageManager
from website.settings import MEDIA_ROOT


class UserConnectTest(TransactionTestCase):

    def __init__(self, methodName=''):
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

    def __randomLogin(self, nam, pwd):
        msg1 = "Please enter a correct username and password."
        msg2 = "Note that both fields may be case-sensitive."
        username = nam
        password = pwd
        response = self.__login(username, password)
        user     = response.context['user']
        self.assertContains(response, msg1)
        self.assertContains(response, msg2)
        self.assertEqual(user.__class__, AnonymousUser)

    def __userLogin(self):
        profile_url = PageManager().get_URL("profile")
        response = self.__login("user_1", "pass_1")
        # Check the good redirection
        self.assertRedirects(response, profile_url)
        response = self.client.get(profile_url)
        # Check profile view contains user
        self.assertIn('user', response.context.keys())
        user = response.context['user']
        # Check the user object has the correct class
        self.assertEqual(user.__class__, UserDC)
        # Check the user is the one
        self.assertEqual(user.id, 2)

    def __init_update_data(self, user, field=None, new_value=None):
        data = {
            "username": user.username,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "icon": user.icon,
            "description": user.description
        }
        if field != None:
            data[field] = new_value
        return data

    def __update_info(self, update_data):
        # go to update page
        update_url = PageManager().get_URL('update')
        profile_url = PageManager().get_URL('profile')
        response = self.client.get(update_url)
        self.assertEqual(response.status_code, 200)
        # get user and default values
        user = response.context['user']
        data = {
            "first_name": user.first_name,
            "last_name": user.last_name,
            "description": user.description,
        }
        # check default values for user_1
        self.assertEqual(user.first_name, '')
        self.assertEqual(user.last_name, '')
        self.assertEqual(user.icon, '')
        self.assertEqual(user.description, '')
        # Update each data
        for field in update_data:
            # update value
            data[field]   = update_data[field]
            compare_value = update_data[field]
            # prepare image if needed
            if field == 'icon':
                compare_value = f'icons/users/{user.username}/{user.username}_icon.png'
                img_path = os.path.join(MEDIA_ROOT, update_data[field])
                data[field] = SimpleUploadedFile(
                    name=img_path,
                    content=open(img_path, 'rb').read(),
                    content_type='image/png')
            # post data
            response = self.client.post(update_url, data)
            # Check redirect
            self.assertRedirects(response, profile_url)
            # Display new info
            response = self.client.get(profile_url)
            self.assertEqual(response.status_code, 200)
            # Get user
            user = response.context['user']
            self.assertTrue(hasattr(user, field))
            self.assertEquals(getattr(user, field), compare_value)
            print(user.icon)

    def test_user_connect(self):
        # Check random user name and password
        with self.subTest("random log/pass"):
            nam = ''.join(random.choice(string.ascii_lowercase) for i in range(8))
            pwd = ''.join(random.choice(string.ascii_lowercase) for i in range(8))
            self.__randomLogin(nam, pwd)
        # Check good user name and random password
        with self.subTest("user_1 + random pass"):
            nam = "user_1"
            pwd = ''.join(random.choice(string.ascii_lowercase) for i in range(8))
            self.__randomLogin(nam, pwd)
        # Check random user name and known password
        with self.subTest("user_1 + random pass"):
            nam = ''.join(random.choice(string.ascii_lowercase) for i in range(8))
            pwd = "pass_1"
            self.__randomLogin(nam, pwd)
        # Check admin user
        with self.subTest("user_1"):
            self.__userLogin()

    def test_user_update(self):
        # Check user connection
        with self.subTest("connect user_1"):
            self.__userLogin()
        # prepare update structure
        data = {
            "first_name" : 'first_1',
            "last_name"  : 'last_1',
            "description": 'description_1',
            "icon"       : 'icons/groups/group_everyone.png',
        }
        self.__update_info(data)








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
