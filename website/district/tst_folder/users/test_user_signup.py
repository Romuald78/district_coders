from django.test import TransactionTestCase
from django.core import management

from toolbox.utils.route_mgr import PageManager


class UserConnectTest(TransactionTestCase):

    def __test_signup(self, nam, pwd, pwd2, email, err_msgs=[]):
        data = {
            'username' : nam,
            'password' : pwd,
            'password2': pwd2,
            'email'    : email,
        }
        response = self.client.post(self.signup_url, data)
        self.assertEquals(response.status_code, 200)
        # TODO : retrieve field information
        # to check the related error
        #print(response.context['form'].fields['username'])
        .........
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
        self.__test_signup('', '', '', '')

    def __one_field(self):
        # username
        self.__test_signup(self.name, '', '', '')
        # pass1
        self.__test_signup('', self.pass_strong, '', '')
        # pass2
        self.__test_signup('', '', self.pass_strong, '')
        # email
        self.__test_signup('', '', '', self.email)

    def __empty_name(self):
        self.__test_signup('', self.pass_strong, self.pass_strong, self.email)

    def __empty_pass(self):
        self.__test_signup('', '', '', '')

    def __empty_email(self):
        self.__test_signup('', '', '', '')

    def __different_pass(self):
        self.__test_signup('', '', '', '')

    def __weak_pass(self):
        self.__test_signup('', '', '', '')

    def existing_user(self):
        self.__test_signup('', '', '', '')

    def existing_email(self):
        self.__test_signup('', '', '', '')
