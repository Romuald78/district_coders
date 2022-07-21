from django.test import TransactionTestCase
from django.core import management

from toolbox.utils.route_mgr import PageManager


class UserConnectTest(TransactionTestCase):

    def __test_signup(self, nam, pwd, pwd2, email):
        data = {
            'username' : nam,
            'password' : pwd,
            'password2': pwd2,
            'email'    : email,
        }
        response = self.client.post(self.signup_url, data)
        return response

    def __check_error(self, response, err_msgs=[]):
        self.assertEquals(response.status_code, 200)
        for msg in err_msgs:
            self.assertTrue(msg in response.content.decode())

    def __init__(self, methodName=''):
        super().__init__(methodName)
        self.signup_url  = PageManager().get_URL('signup')
        self.name        = 'user_999'
        self.pass_weak   = 'pass_999'
        self.pass_strong = 'pass_999_AB12$'
        self.email       = 'email999@toto.fr'

    def setUp(self):
        # in django the client is instanciated in _pre_setup()
        #self.client  = Client()
        management.call_command("dc_reinit")
        management.call_command("populate_multi")

    def test_user_signup(self):
        process = [
            # New user and new email
            "empty_form",
            "one_field",    # username, password1, password2, email
            "empty_name",
            "empty_pass",
            "empty_email",
            "different_pass", # no pass2, different pass2, one char less/more
            # Valid forms but ...
            "weak_pass",
            "existing_user",
            "existing_email",
            # Valid subscription
            ###"valid_form"
        ]
        for p in process:
            method = [f for f in dir(self.__class__) if callable(getattr(self.__class__, f)) and p in f]
            if len(method) > 0:
                with self.subTest(p):
                    f = getattr(self.__class__, method[0])
                    f(self)

    # ----------------------------------------------------

    def __empty_form(self):
        response = self.__test_signup('', '', '', '')
        self.__check_error(response, ['This field is required.'])

    def __one_field(self):
        # username
        response = self.__test_signup(self.name, '', '', '')
        self.__check_error(response, ['This field is required.'])
        # pass1
        response = self.__test_signup('', self.pass_strong, '', '')
        self.__check_error(response, ['This field is required.'])
        # pass2
        response = self.__test_signup('', '', self.pass_strong, '')
        self.__check_error(response, ['This field is required.'])
        # email
        response = self.__test_signup('', '', '', self.email)
        self.__check_error(response, ['This field is required.'])

    def __empty_name(self):
        response = self.__test_signup('', self.pass_strong, self.pass_strong, self.email)
        self.__check_error(response)
        a = response.context['form']
        print(a.form)

    def __empty_pass(self):
        response = self.__test_signup('', '', '', '')
        self.__check_error(response)

    def __empty_email(self):
        response = self.__test_signup('', '', '', '')
        self.__check_error(response)

    def __different_pass(self):
        response = self.__test_signup('', '', '', '')
        self.__check_error(response)

    def __weak_pass(self):
        response = self.__test_signup('', '', '', '')
        self.__check_error(response)

    def existing_user(self):
        response = self.__test_signup('', '', '', '')
        self.__check_error(response)

    def existing_email(self):
        response = self.__test_signup('', '', '', '')
        self.__check_error(response)
