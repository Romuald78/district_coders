import inspect
import os
import random
import string
import json

from django.contrib.auth.models import AnonymousUser
from django.core import management
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse

from config.constants.error_message_cnf import ERROR_CODE_CONFLICT, GROUP_REGISTER_ALREADY_IN, ERROR_CODE_PARAMS, \
    GROUP_REGISTER_EMPTY_KEY, ERROR_CODE_NOT_FOUND, GROUP_REGISTER_INVALID_KEY
from district.models.group import GroupDC
from district.models.user import UserDC
from district.tst_folder.core.tst_main_class import MainClassTest
from toolbox.utils.route_mgr import PageManager
from website.settings import MEDIA_ROOT, DEFAULT_GROUP_KEY
from bs4 import BeautifulSoup

class UserUpdateTest(MainClassTest):

    def __init__(self, methodName=''):
        super().__init__(methodName)
        self.name_valid = 'user_1'
        self.pass_valid = 'pass_1'
        self.valid_Id = 2

    def setUp(self):
        management.call_command("dc_reinit")
        management.call_command("populate_multi")

    @staticmethod
    def getSortedTestCaseNames():
        return ["test_user_update"]

    def test_user_update(self):
        self.__update_fields()


    def __check_display(self):
        update_url = reverse('update', kwargs={'user_id': self.valid_Id})
        self.__userLogin()

        response = self.client.get(update_url)
        user = response.context['user']
        self.assertEquals(response.status_code, 200)

        soup = BeautifulSoup(response.content, 'html.parser')
        soup_user = soup.find(attrs={"name": "username"})
        value = soup_user.get("value", "")
        self.assertEquals(user.username, value)

        for field_name in ["first_name", "last_name", "description"]:
            soup_user = soup.find(attrs={"name": field_name})
            html_value = soup_user.get("value", "")
            attr_value = getattr(user, field_name)
            if attr_value is None:
                self.assertEquals(html_value, "")
            else:
                self.assertEquals(attr_value, html_value)

    def __update_fields(self):
        update_url = reverse('update', kwargs={'user_id': self.valid_Id})
        profile_url = PageManager().get_URL('profile')

        with self.subTest("display update"):
            self.__check_display()


        update_data = {
            "username": self.name_valid,
            "first_name": 'first_1',
            "last_name": 'last_1',
            "description": 'description_1',
            "icon": 'icons/groups/group_everyone.png',
        }

        data = {
            "username": self.name_valid,
            "first_name": '',
            "last_name": '',
            "description": '',
        }

        for field in update_data:
            with self.subTest(f"update {field}"):
                # To verif the value in user account
                self.__check_display()

                # Post and redirect
                data[field] = update_data[field]
                compare_value = update_data[field]

                if field == 'icon':
                    compare_value = f'icons/users/{user.username}/{user.username}_icon.png'
                    img_path = os.path.join(MEDIA_ROOT, update_data[field])
                    data[field] = SimpleUploadedFile(
                        name=str(img_path),
                        content=open(img_path, 'rb').read(),
                        content_type='image/png'
                    )

                response = self.client.post(update_url, data)
                self.assertRedirects(response, profile_url)

                response = self.client.get(profile_url)
                self.assertEquals(response.status_code, 200)
                user = response.context['user']
                self.assertTrue(hasattr(user, field))
                self.assertEquals(getattr(user, field), compare_value)

    def __userLogin(self):
        # login_url = PageManager().get_URL('login')
        # data = {
        #     'username': self.name_valid,
        #     'password': self.pass_valid,
        # }
        # response = self.client.post(login_url, data, follow=True)
        # self.assertRedirects(response, reverse('profile'))
        # user = response.context['user']
        # self.assertTrue(user.is_authenticated)
        # self.assertEquals(user.__class__, UserDC)
        connected = self.client.login(username=self.name_valid, password=self.pass_valid)
        self.assertTrue(connected)
