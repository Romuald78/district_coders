import inspect
import os
import random
import string
import json

from django.contrib.auth.models import AnonymousUser
from django.core import management
from django.urls import reverse

from config.constants.error_message_cnf import ERROR_CODE_CONFLICT, GROUP_REGISTER_ALREADY_IN, ERROR_CODE_PARAMS, \
    GROUP_REGISTER_EMPTY_KEY, ERROR_CODE_NOT_FOUND, GROUP_REGISTER_INVALID_KEY
from district.models.group import GroupDC
from district.models.user import UserDC
from district.tst_folder.core.tst_main_class import MainClassTest
from toolbox.utils.route_mgr import PageManager
from website.settings import DEFAULT_GROUP_KEY

class UserGroupRegisterTest(MainClassTest):

    def __init__(self, methodName=''):
        super().__init__(methodName)
        self.json_url = PageManager().get_URL('group_register')
        self.name_valid = "user_1"
        self.pass_valid = "pass_1"

        self.empty_key = ""
        self.random_key = ''.join(random.choice(string.ascii_lowercase) for _ in range(8))

        self.error_empty_key = GROUP_REGISTER_EMPTY_KEY
        self.error_invalid_key = GROUP_REGISTER_INVALID_KEY
        self.error_conflict = GROUP_REGISTER_ALREADY_IN

        self.code_empty_key = ERROR_CODE_PARAMS
        self.code_invalid_key = ERROR_CODE_NOT_FOUND
        self.code_conflict = ERROR_CODE_CONFLICT

        self.success_code = 0

        self.default_group = GroupDC.objects.filter(register_key=DEFAULT_GROUP_KEY).first()
        self.all_users = list(UserDC.objects.filter(id__gt=0).all())
        self.all_groups = list(GroupDC.objects.all())

    def setUp(self):
        management.call_command("dc_reinit")
        management.call_command("populate_multi")

    @staticmethod
    def getSortedTestCaseNames():
        return ["test_group_register"]

    def test_group_register(self):
        for user in self.all_users:
            if user.is_staff:
                continue
            self.current_user = user
            plain_pwd = "pass_"+user.username.split("_")[1]

            process = [
                "empty_key",
                "random_key_test",
                "check_everyone_group",
                "register_groups"
            ]
            for p in process:
                method = [f for f in dir(self.__class__) if callable(getattr(self.__class__, f)) and p in f]
                if len(method) > 0:
                    with self.subTest(f"{p} : {user.username}"):
                        self.client.logout()
                        self.client.login(username=user.username, password=plain_pwd)

                        f = getattr(self.__class__, method[0])
                        try:
                            f(self)
                        except AssertionError as ae:
                            msg = f"\n-------------\n[ERROR] in method '{f.__name__}'\n-------------"
                            raise AssertionError(str(ae) + msg)

    # -------------------------
    # Private test methods
    # -------------------------

    def __empty_key(self):
        self.__post_and_assert(self.empty_key, self.code_empty_key, self.error_empty_key)

    def __random_key_test(self):
        self.__post_and_assert(self.random_key, self.code_invalid_key, self.error_invalid_key)

    def __check_everyone_group(self):
        user = self.current_user
        eo_grp = self.default_group
        self.assertIsNotNone(eo_grp)
        usr_grp = user.groups.filter(id=eo_grp.id).first()
        if user.is_staff:
            self.assertIsNone(usr_grp)
        else:
            self.assertEqual(eo_grp, usr_grp)

    def __register_groups(self):
        user = self.current_user
        for group in self.all_groups:
            already_in_group = user.groups.filter(id=group.id).exists()

            if not already_in_group:

                self.__post_and_assert(group.register_key, self.success_code, None)

            self.__post_and_assert(group.register_key, self.code_conflict, self.error_conflict)

    # -------------------------
    # Generic JSON post + assert
    # -------------------------

    def __post_and_assert(self, key, expected_code, expected_msg):

        response = self.client.post(self.json_url, {"register_key": key})


        # Vérification standard
        self.assertEqual(response.status_code, 200)

        json_result = json.loads(response.content)
        self.assertEqual(json_result.get("exit_code"), expected_code)

        if expected_msg is not None:
            self.assertEqual(json_result.get("err_msg"), expected_msg)

