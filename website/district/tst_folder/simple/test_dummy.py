from django.contrib.auth.models import AnonymousUser
from django.core import management
from django.test import SimpleTestCase, RequestFactory, TransactionTestCase
from django.urls import reverse

from district.controllers.ctrl_assessment import ctrl_asse_details
from district.controllers.ctrl_exercise import ctrl_exercise_details, ctrl_exercise_write
from district.controllers.ctrl_main import ctrl_home
from district.controllers.ctrl_user import ctrl_user_profile
from district.models.assessment import Assessment
from district.models.exercise import Exercise
from district.models.exo2test import Exo2Test
from district.models.inspector_mode import InspectorMode
from toolbox.migration_tools.debug_data import debug_migration
from toolbox.migration_tools.migration_group import group_migration
from toolbox.migration_tools.migration_inspect_mode import mode_migration
from toolbox.migration_tools.migration_language import language_migration


class SimpleTest(TransactionTestCase):
    reset_sequences = True

    def __init__(self, methodName='test_all'):
        super().__init__(methodName)
        self.databases = False

    def setUp(self):
        self.serialized_rollback = True

        print("peupler ?", not self.databases)
        # Every test needs access to the request factory.
        self.factory = RequestFactory()
        if not self.databases:
            print("Let's go populate the db")
            self.databases = True
            management.call_command("makemigrations")
            management.call_command("migrate")
            management.call_command("populate")
            # InspectorMode.objects.create(name="dansmontest")

    def test_all(self):
        # self.Test_user_profile()
        # self.Test_home()
        # self.Test_assessment_details()
        # self.Test_exercise_details()
        # self.Test_exercise_write()
        pass

    def test_user_profile(self):
        request = self.factory.get("/accounts/profile")
        request.user = AnonymousUser()
        response = ctrl_user_profile(request)
        self.assertEqual(response.status_code, 302)

    def test_home(self):
        request = self.factory.get("/")
        request.user = AnonymousUser()
        response = ctrl_home(request)
        self.assertEqual(response.status_code, 200)

    def test_assessment_details(self):
        print("number assessment", len(Assessment.objects.all()))
        asse = Assessment.objects.all().first()
        request = self.factory.get(reverse('assessment_details', args=[asse.id]))
        request.user = AnonymousUser()
        response = ctrl_asse_details(request)
        self.assertEqual(response.status_code, 302)

    def test_exercise_details(self):
        ex2tst = Exo2Test.objects.first()
        asse = Assessment.objects.first()
        request = self.factory.get(reverse('exercise_details', kwargs={"extest": ex2tst.id, "asse": asse.id}))
        request.user = AnonymousUser()
        response = ctrl_exercise_details(request)
        self.assertEqual(response.status_code, 302)

    def test_exercise_write(self):
        ex2tst = Exo2Test.objects.first()
        asse = Assessment.objects.first()
        request = self.factory.get(reverse('exercise_write', kwargs={"extest": ex2tst.id, "asse": asse.id}))
        request.user = AnonymousUser()
        response = ctrl_exercise_write(request)
        self.assertEqual(response.status_code, 302)