import json

from django.contrib.auth.models import AnonymousUser
from django.test import TransactionTestCase, RequestFactory
from django.urls import reverse

from config.constants.route_cnf import PAGES
from district.models.group import GroupDC
from district.models.user import UserDC
from toolbox.utils.route_mgr import PageManager


class AnonymousTest(TransactionTestCase):

    def __init__(self, methodName='test_all'):
        print(f"\33[38;2;0;255;0m INIT {methodName}\33[0m")
        super().__init__(methodName)

    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()

    # python manage.py test district.tst_folder.simple.test_anonymous
    def test_no_params(self):
        for page in PAGES:
            if not page.params and page.type == "view":
                print(f"[TEST PAGE] {page.name}")
                with self.subTest():
                    request = self.factory.get(reverse(page.name))
                    request.user = AnonymousUser()
                    response = page.ctrl(request)
                    if page.log_req:
                        self.assertEqual(response.status_code, 302)
                        # self.assertRedirects(response, '')
                    else:
                        self.assertEqual(response.status_code, 200)

    def test_email_change_confirm(self):
        page = PageManager().get_page("email_change_confirm")

        # test with id of user that didn't validate its email
        with self.subTest():
            user1 = UserDC.objects.create(username="user1", first_name="pf1", last_name="pl1", email="jsp@jsp1.com", is_active=True,
                                          is_email_validated=False)

            request = self.factory.get(reverse(page.name, kwargs={"user_id": user1.id}))
            request.user = AnonymousUser()
            response = page.ctrl(request, user1.id)
            self.assertEqual(response.status_code, 200)

        # test with id of user that did validate its email
        with self.subTest():
            user2 = UserDC.objects.create(username="user2", first_name="pf2", last_name="pl2", email="jsp@jsp2.com", is_active=True,
                                          is_email_validated=True)

            request = self.factory.get(reverse(page.name, kwargs={"user_id": user2.id}))
            request.user = AnonymousUser()
            response = page.ctrl(request, user2.id)
            self.assertEqual(response.status_code, 302)

        # test with random id
        with self.subTest():
            rand_id = 3000
            request = self.factory.get(reverse(page.name, kwargs={"user_id": rand_id}))
            request.user = AnonymousUser()
            response = page.ctrl(request, rand_id)
            self.assertEqual(response.status_code, 302)

    def test_json_group_register(self):
        pass
        # pm = PageManager()
        # page = pm.get_page('group_register')
        #
        # request = self.client.post(page.url, {"register_key": "Robert De Niro"})
        # request.user = AnonymousUser()
        # response = page.ctrl(request)
        #
        # self.assertRedirects(request, "/accounts/login/")



# Page('group_register', 'accounts/group_register/', ctrl_json_user_register, type="json", parameters=True),
# Page('my_groups', 'accounts/my_groups/', ctrl_json_user_groups, type="json"),
#
# Page('email_change_confirm', 'accounts/email_change_confirm/<int:user_id>/', ctrl_email_verification, log_req=False, parameters=True),
# Page('email_change_send', 'accounts/email_change_send/', ctrl_json_sending_email, type="json", log_req=False),
# Page('exercise_inspect', 'exercise/inspect/', ctrl_json_exercise_inspect, type='json', parameters=True),
# Page('exercise_stats', 'exercise/stats/', ctrl_json_testresult_exists, type='json', parameters=True),










