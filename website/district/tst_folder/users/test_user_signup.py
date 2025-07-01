import sys

from django.test import TransactionTestCase
from django.core import management
from django.urls import reverse

from district.tst_folder.core.tst_main_class import MainClassTest
from toolbox.utils.route_mgr import PageManager


class UserConnectTest(MainClassTest):

    ERR_FLD_REQ     = 'This field is required'
    ERR_EMPTY_MAIL  = 'Empty email'
    ERR_PWD_COMMON  = 'This password is too common'
    ERR_PWD_SHORT   = 'This password is too short'
    ERR_PWD_8CHARS  = 'It must contain at least 8 characters'
    ERR_PWD_NUMERIC = 'This password is entirely numeric'
    ERR_PWD_MATCH   = "The two password fields didn"
    ERR_USER_EXISTS = 'A user with that username already exists.'
    ERR_MAIL_EXISTS = 'This email is already in use'

    def __empty_form(self):
        msg = [UserConnectTest.ERR_FLD_REQ,
               UserConnectTest.ERR_EMPTY_MAIL]
        self.__test_signup('', '', '', '', msg)

    def __one_field(self):
        # username
        msg = [UserConnectTest.ERR_FLD_REQ,
               UserConnectTest.ERR_EMPTY_MAIL]
        self.__test_signup(self.name, '', '', '', msg)
        # pass1
        self.__test_signup('', self.pass_strong, '', '', msg)
        self.__test_signup('', '', self.pass_strong, '', msg)
        # pass numeric
        msg = [UserConnectTest.ERR_FLD_REQ,
               UserConnectTest.ERR_EMPTY_MAIL,
               UserConnectTest.ERR_PWD_NUMERIC]
        self.__test_signup('', '', self.pass_numeric, '', msg)
        # pass common
        msg = [UserConnectTest.ERR_FLD_REQ,
               UserConnectTest.ERR_EMPTY_MAIL,
               UserConnectTest.ERR_PWD_COMMON]
        self.__test_signup('', '', self.pass_common, '', msg)
        # pass numeric small
        msg = [UserConnectTest.ERR_FLD_REQ,
               UserConnectTest.ERR_EMPTY_MAIL,
               UserConnectTest.ERR_PWD_NUMERIC,
               UserConnectTest.ERR_PWD_SHORT,
               UserConnectTest.ERR_PWD_8CHARS]
        self.__test_signup('', '', self.pass_numeric[:4], '', msg)
        # pass common small
        msg = [UserConnectTest.ERR_FLD_REQ,
               UserConnectTest.ERR_EMPTY_MAIL,
               UserConnectTest.ERR_PWD_SHORT,
               UserConnectTest.ERR_PWD_8CHARS]
        self.__test_signup('', '', self.pass_common[:4], '', msg)
        # email
        msg = [UserConnectTest.ERR_FLD_REQ]
        self.__test_signup('', '', '', self.email, msg)

    def __empty_name(self):
        msg = [UserConnectTest.ERR_FLD_REQ]
        self.__test_signup('', self.pass_strong, self.pass_strong, self.email, msg)

    def __empty_pass(self):
        msg = [UserConnectTest.ERR_FLD_REQ]
        self.__test_signup(self.name, '', '', self.email, msg)
        self.__test_signup(self.name, self.pass_strong, '', self.email, msg)
        self.__test_signup(self.name, '', self.pass_strong, self.email, msg)

    def __empty_email(self):
        msg = [UserConnectTest.ERR_EMPTY_MAIL]
        self.__test_signup(self.name, self.pass_strong, self.pass_strong, '', msg)

    def __different_pass(self):
        msg = [UserConnectTest.ERR_PWD_MATCH]
        self.__test_signup(self.name, self.pass_strong, self.pass_strong+"oo", self.email, msg)
        self.__test_signup(self.name, self.pass_strong+"oo", self.pass_strong, self.email, msg)

    def __weak_pass(self):
        msg = [UserConnectTest.ERR_PWD_SHORT, UserConnectTest.ERR_PWD_8CHARS]
        self.__test_signup(self.name, self.pass_weak, self.pass_weak, self.email, msg)
        msg = [UserConnectTest.ERR_PWD_COMMON]
        self.__test_signup(self.name, self.pass_common, self.pass_common, self.email, msg)
        msg = [UserConnectTest.ERR_PWD_NUMERIC]
        self.__test_signup(self.name, self.pass_numeric, self.pass_numeric, self.email, msg)

    def existing_user(self):
        msg = [UserConnectTest.ERR_USER_EXISTS]
        self.__test_signup('user_1', self.pass_strong, self.pass_strong, self.email, msg)

    def existing_email(self):
        msg = [UserConnectTest.ERR_MAIL_EXISTS]
        self.__test_signup(self.name, self.pass_strong, self.pass_strong, 'user_1@dummy.com', msg)

    def __correct_signup(self):
        self.__test_signup(self.name, self.pass_strong, self.pass_strong, self.email, err_msgs=None)


    def __test_signup(self, nam, pwd, pwd2, email, err_msgs=["xxx"]):
        data = {
            'username' : nam,
            'password1' : pwd,
            'password2': pwd2,
            'email'    : email,
        }
        response = self.client.post(self.signup_url, data)
        if err_msgs is not None:
            self.assertEquals(response.status_code, 200)
        else :
            expected_url = reverse('email_change_confirm', kwargs={'user_id': 17})
            self.assertRedirects(response, expected_url)

        # TODO : retrieve field information
        # to check the related error
        #print(response.context['form'].fields['username'])

        if err_msgs is not None:
            for msg in err_msgs:
                found = msg in response.content.decode()
                if not found:
                    print(response.content.decode(), file=sys.stderr)
                self.assertTrue(found, f"{msg} has not been found !")


    def __init__(self, methodName=''):
        super().__init__(methodName)
        self.signup_url   = PageManager().get_URL('signup')
        self.name         = 'user_999'
        self.pass_weak    = 'pass_9'
        self.pass_common  = 'abcdefghij'
        self.pass_numeric = '1234567890'
        self.pass_strong  = 'pass_999_AB12$'
        self.email        = 'email999@toto.fr'

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
            "correct_signup"
        ]
        for p in process:
            method = [f for f in dir(self.__class__) if callable(getattr(self.__class__, f)) and p in f]
            if len(method) > 0:
                with self.subTest(p):
                    f = getattr(self.__class__, method[0])
                    try:
                        f(self)
                    except AssertionError as ae:
                        msg = f"\n-------------\n[ERROR] in method '{f.__name__}'\n-------------"
                        raise AssertionError(str(ae) + msg)

    # ----------------------------------------------------



