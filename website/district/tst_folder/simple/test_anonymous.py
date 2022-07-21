import json

from django.contrib.auth.models import AnonymousUser
from django.test import TransactionTestCase, RequestFactory
from django.urls import reverse

from config.constants.route_cnf import PAGES
from district.models.user import UserDC
from toolbox.utils.route_mgr import PageManager


class AnonymousTest(TransactionTestCase):

    def __init__(self, methodName='test_no_params'):
        print(f"\33[38;2;0;255;0m INIT {methodName}\33[0m")
        super().__init__(methodName)

    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()

    # python manage.py test district.tst_folder.simple.test_anonymous
    def test_no_params(self):
        for page in PAGES:
            if not page.params:
                # print(f"[TEST PAGE] {page.name}")
                with self.subTest(page.url):
                    response = self.client.get(reverse(page.name))
                    response.user = AnonymousUser()
                    if page.log_req:
                        self.assertRedirects(response, "/accounts/login/?next=%2F"+page.url.replace("/", "%2F"))
                    else:
                        self.assertEquals(response.status_code, 200)

    def test_email_change_confirm(self):
        page = PageManager().get_page("email_change_confirm")

        # test with id of user that didn't validate its email
        with self.subTest("email validate False"):
            user1 = UserDC.objects.create(username="user1", first_name="pf1", last_name="pl1", email="jsp@jsp1.com", is_active=True,
                                          is_email_validated=False)

            request = self.factory.get(reverse(page.name, kwargs={"user_id": user1.id}))
            request.user = AnonymousUser()
            response = page.ctrl(request, user1.id)
            self.assertEquals(response.status_code, 200)

        # test with id of user that did validate its email
        with self.subTest("email validate True"):
            user2 = UserDC.objects.create(username="user2", first_name="pf2", last_name="pl2", email="jsp@jsp2.com", is_active=True,
                                          is_email_validated=True)

            response = self.client.get(f'/accounts/email_change_confirm/{user2.id}/')
            self.assertIn("controller_error_message", response.context.keys())
        # test with impossible id
        with self.subTest("not existing user"):
            rand_id = 3000
            response = self.client.get(reverse(page.name, kwargs={"user_id": rand_id}))
            self.assertIn("controller_error_message", response.context.keys())

    def test_json_group_register(self):
        page = PageManager().get_page('group_register')
        response = self.client.post(reverse(page.name), {"register_key": "Robert De Niro"})
        self.assertRedirects(response, "/accounts/login/?next=%2F"+page.url.replace("/", "%2F"))

    def test_json_exercise_insepct(self):
        page = PageManager().get_page('exercise_inspect')
        response = self.client.post(reverse(page.name), {
            "ex2tst_id": 1,
            "lang_id": 1,
            "raw_code": "",
            "asse_id": 1,
        })
        self.assertRedirects(response, "/accounts/login/?next=%2F" + page.url.replace("/", "%2F"))

    def test_json_exercise_stats(self):
        page = PageManager().get_page('exercise_inspect')
        response = self.client.post(reverse(page.name), {
            "asse_id": 1,
            "ex2tst_id": 1,
            "lang_id": 1,
        })
        self.assertRedirects(response, "/accounts/login/?next=%2F" + page.url.replace("/", "%2F"))

# Page('email_change_confirm', 'accounts/email_change_confirm/<int:user_id>/', ctrl_email_verification, log_req=False, parameters=True),
# Page('email_change_send', 'accounts/email_change_send/', ctrl_json_sending_email, type="json", log_req=False, param true),
