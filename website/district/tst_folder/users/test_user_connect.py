import os
import random
import string
import json

from django.contrib.auth.models import AnonymousUser
from django.core import management
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TransactionTestCase, RequestFactory, Client

from config.constants.error_message_cnf import ERROR_CODE_CONFLICT, GROUP_REGISTER_ALREADY_IN, ERROR_CODE_PARAMS, \
    GROUP_REGISTER_EMPTY_KEY, ERROR_CODE_NOT_FOUND, GROUP_REGISTER_INVALID_KEY
from district.models.group import GroupDC
from district.models.user import UserDC
from toolbox.utils.route_mgr import PageManager
from website.settings import MEDIA_ROOT, DEFAULT_GROUP_KEY


class UserConnectTest(TransactionTestCase):

    def __init__(self, methodName=''):
        super().__init__(methodName)

    def setUp(self):
        # in django the client is instanciated in _pre_setup()
        #self.client  = Client()
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
        self.assertEquals(user.__class__, AnonymousUser)

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
        self.assertEquals(user.__class__, UserDC)
        # Check the user is the one
        self.assertEquals(user.id, 2)

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
        self.assertEquals(response.status_code, 200)
        # get user and default values
        user = response.context['user']
        data = {
            "first_name": user.first_name,
            "last_name": user.last_name,
            "description": user.description,
        }
        # check default values for user_1
        self.assertEquals(user.first_name, '')
        self.assertEquals(user.last_name, '')
        self.assertEquals(user.icon, '')
        self.assertEquals(user.description, '')
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
            self.assertEquals(response.status_code, 200)
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
        json_url = PageManager().get_URL('group_register')
        for user in UserDC.objects.filter(id__gt=0).all():
            # ----------------------------
            # User login
            # ----------------------------
            self.client.force_login(user)
            # ----------------------------
            # register with Empty key
            # ----------------------------
            with self.subTest(f"usr{user.id} - empty key"):
                response = self.client.post(json_url, {"register_key": ""})
                self.assertEquals(response.status_code, 200)
                json_result = json.loads(response.content)
                self.assertIn('exit_code', json_result)
                self.assertEquals(json_result['exit_code'], ERROR_CODE_PARAMS)
                self.assertIn('err_msg', json_result)
                self.assertEquals(json_result['err_msg'], GROUP_REGISTER_EMPTY_KEY)
            # ----------------------------
            # Register with random key
            # ----------------------------
            with self.subTest(f"usr{user.id} - random key"):
                rand_key = ''.join(random.choice(string.ascii_lowercase) for i in range(8))
                response = self.client.post(json_url, {"register_key": rand_key})
                self.assertEquals(response.status_code, 200)
                json_result = json.loads(response.content)
                self.assertIn('exit_code', json_result)
                self.assertEquals(json_result['exit_code'], ERROR_CODE_NOT_FOUND)
                self.assertIn('err_msg', json_result)
                self.assertEquals(json_result['err_msg'], GROUP_REGISTER_INVALID_KEY)
            # ----------------------------
            # Check already registered to "everyone" group
            # ----------------------------
            # if this is not the admin user
            with self.subTest(f"usr{user.id} - everyone group"):
                eo_grp = GroupDC.objects.filter(register_key=DEFAULT_GROUP_KEY).first()
                self.assertIsNotNone(eo_grp)
                usr_grp = user.groups.filter(id=eo_grp.id).first()
                # The admin user is not linked to the "everyone" group
                if user.is_staff:
                    self.assertEquals(None, usr_grp)
                else:
                    self.assertEquals(eo_grp, usr_grp)
            # ----------------------------
            # Connect this user to any group
            # ----------------------------
            for group in GroupDC.objects.all():
                # Store information about user/group link
                in_group = user.groups.filter(id=group.id)
                with self.subTest(f"usr{user.id} - grp{group.id} - register"):
                    # Here we check the group is not linked
                    if not in_group:
                        # link the user and the group
                        response = self.client.post(json_url, {"register_key": group.register_key})
                        self.assertEquals(response.status_code, 200)
                        json_result = json.loads(response.content)
                        self.assertIn('exit_code', json_result)
                        self.assertEquals(json_result['exit_code'], 0)
                    # Here we can be sure there is a link between the user and the group
                    # Check to link a second time
                    response = self.client.post(json_url, {"register_key": group.register_key})
                    self.assertEquals(response.status_code, 200)
                    json_result = json.loads(response.content)
                    self.assertIn('exit_code', json_result)
                    self.assertEquals(json_result['exit_code'], ERROR_CODE_CONFLICT)
                    self.assertIn('err_msg', json_result)
                    self.assertEquals(json_result['err_msg'], GROUP_REGISTER_ALREADY_IN)
