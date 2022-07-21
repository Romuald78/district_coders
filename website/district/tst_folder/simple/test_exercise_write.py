import json

from django.core import management
from django.test import TransactionTestCase, RequestFactory
from django.urls import reverse

from config.constants.error_message_cnf import ERROR_CODE_OK
from district.controllers.ctrl_exercise import ctrl_json_exercise_get_stat
from district.models.exotest2lang import ExoTest2Lang
from district.models.language import Language
from district.models.testresult import TestResult
from district.tst_folder.simple.assets.test_case_getter import get_param_lang


class ExerciseWriteTest(TransactionTestCase):

    def __init__(self, methodName='test_stat_solve_code'):
        super().__init__(methodName)

    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()
        # clear and populate the db
        management.call_command("dc_reinit")
        management.call_command("populate_multi")

        # solve one exercise in C++
        (user, extst, asse) = get_param_lang()
        extstlng = ExoTest2Lang.objects.get(exo2test=extst, lang__name="C++")
        TestResult.objects.create(
            exo_test2lang=extstlng,
            user=user,
            solve_code=extstlng.lang.default_code,
            solve_percentage=100.0,
            assessment=asse
        )

    def test_stat_solve_code(self):
        (user, extst, asse) = get_param_lang()

        # let's test every languages available
        for lang in Language.objects.filter(exotest2lang__exo2test=extst, exotest2lang__exo2test__test__assessment=asse).all():
            info = f"lang{lang.id}:{lang.name}"
            request = self.factory.post(reverse('exercise_stats_get'),
                                        {
                                            "ex2tst_id": extst.id,
                                            "asse_id": asse.id,
                                            "lang_id": lang.id})
            request.user = user
            response = ctrl_json_exercise_get_stat(request)
            dict_json = json.loads(response.content)
            # check if test result exist
            tstres_all = TestResult.objects.filter(exo_test2lang__lang_id=lang.id, exo_test2lang__exo2test_id=extst.id, assessment_id=asse.id)
            if tstres_all.exists():
                tstres_db = tstres_all.first()
                tstres_res = None
                for i in dict_json["testresult"]:
                    if i["lang_obj"]["name"] == lang.name:
                        tstres_res = i["testresult_obj"]

                with self.subTest(f"{info}: solve code"):
                    self.assertEquals(tstres_db.solve_code, tstres_res["solve_code"])
                with self.subTest(f"{info}: solve percentage"):
                    self.assertGreater(tstres_res["solve_percentage"], 0.0)
                with self.subTest(f"{info}: exit code"):
                    self.assertEquals(dict_json["exit_code"], ERROR_CODE_OK)
            else:
                with self.subTest(f"{info}: solve code"):
                    self.assertNotIn(lang.name, [i["lang_obj"].name for i in dict_json["testresult"]])
                with self.subTest(f"{info}: exit code"):
                    self.assertEquals(dict_json["exit_code"], ERROR_CODE_OK)

