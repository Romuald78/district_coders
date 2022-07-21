import json
import os.path

from django.core import management
from django.test import TransactionTestCase, RequestFactory
from django.urls import reverse
from django.utils import timezone

from config.constants.default_value_cnf import EX_INSPECT_ERROR_RANGE_MIN
from config.constants.error_message_cnf import USER_RAW_CODE_TOO_BIG, ERROR_CODE_ACCESS, \
    ERROR_CODE_COMPILE, COMPILE_ERROR, ERROR_CODE_TIMEOUT, ERROR_CODE_UNSUPPORTED
from district.controllers.ctrl_exercise import ctrl_json_exercise_inspect, ctrl_json_exercise_get_stat
from district.models.assessment import Assessment
from district.models.exo2test import Exo2Test
from district.models.language import Language
from district.models.user import UserDC
from district.tst_folder.simple.assets.test_case_getter import get_param_lang


class ExerciseInspectorTest(TransactionTestCase):

    def __init__(self, methodName='test_user_access'):
        self.lang = ["C", "JS", "PHP", "Python"]
        self.lang_meta = {"C": {"extension": "c", "is_compiled": True},
                          "JS": {"extension": "js", "is_compiled": False},
                          "PHP": {"extension": "php", "is_compiled": False},
                          "Python": {"extension": "py", "is_compiled": False},
                          }

        self.CODE_TEST_OK = 1
        self.CODE_TEST_NOK = 2
        self.CODE_TEST_EMPTY = 3
        self.CODE_TEST_SYNTAX = 4
        self.CODE_TEST_INF_LOOP = 5
        self.CODE_TEST_NOT_TOO_LONG = 6
        self.CODE_TEST_TOO_LONG = 7
        super().__init__(methodName)

    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()
        # clear and populate the db
        management.call_command("dc_reinit")
        management.call_command("populate_multi")

    def get_test_file(self, lang, code_test):
        if lang.name in self.lang:
            # get test file
            case = ""
            if code_test == self.CODE_TEST_OK:
                case = "ok"
            elif code_test == self.CODE_TEST_NOK:
                case = "nok"
            elif code_test == self.CODE_TEST_EMPTY:
                case = "empty"
            elif code_test == self.CODE_TEST_SYNTAX:
                case = "syntax"
            elif code_test == self.CODE_TEST_INF_LOOP:
                case = "loop"
            elif code_test == self.CODE_TEST_NOT_TOO_LONG:
                case = "not_long"
            elif code_test == self.CODE_TEST_TOO_LONG:
                case = "long"

            return f"ex_val_abs-{case}.{self.lang_meta[lang.name]['extension']}.txt"

        return None

    # python manage.py test district.tst_folder.simple.test_exercise_inspector.ExerciseInspectorTest.test_user_access -v 2 --failfast
    def test_user_access(self):
        for asse_item in Assessment.objects.all():
            for curr_user in UserDC.objects.all():
                rank_access = True
                for ex2tst_item in Exo2Test.objects.order_by("rank").all():
                    asse_qs = Assessment.objects.filter(test__exo2test=ex2tst_item, groups__userdc=curr_user, id=asse_item.id)
                    do_access = asse_qs.exists()
                    do_see = asse_qs.exists()
                    err_msg = "VALID"
                    if do_access:
                        other_asse = Assessment.objects.filter(test__exo2test=ex2tst_item, groups__userdc=curr_user)
                        # check if there are assessments in process
                        if other_asse.filter(start_time__lte=timezone.now(), end_time__gt=timezone.now()).exists():
                            # check if the current assessment is in process
                            if asse_item.start_time.__le__(timezone.now()) and asse_item.end_time.__gt__(timezone.now()):
                                if rank_access:
                                    # either solve_percentage_req = 0
                                    # either solver_percentage_req <= solve_percentage
                                    is_there_extstlng = ex2tst_item.exotest2lang_set.exists()
                                    if is_there_extstlng:
                                        test_result_not_nul = ex2tst_item.exotest2lang_set.order_by("-testresult__solve_percentage").first()
                                        is_there_testresult = test_result_not_nul.testresult_set.exists()
                                        if is_there_testresult:
                                            is_solve_percentage_valid = test_result_not_nul.testresult_set.first().solve_percentage >= ex2tst_item.solve_percentage_req
                                        else:
                                            is_solve_percentage_valid = False
                                    else:
                                        is_there_testresult = False
                                        is_solve_percentage_valid = False

                                    condition = ex2tst_item.solve_percentage_req == 0 or (
                                        is_there_extstlng and
                                        is_there_testresult and
                                        is_solve_percentage_valid
                                    )
                                    if not condition:
                                        rank_access = False
                                else:
                                    do_access = False
                                    err_msg = "Rank not valid"
                            else:
                                do_access = False
                                # if the current assessment is past but not in training mode or future
                                if (asse_item.start_time.__lt__(timezone.now()) and asse_item.end_time.__le__(timezone.now())\
                                        and asse_item.training_time.__gt__(timezone.now()))\
                                        or (asse_item.start_time.__gt__(timezone.now()) and asse_item.end_time.__gt__(timezone.now())\
                                        and asse_item.training_time.__gt__(timezone.now())):
                                    do_see = False
                                err_msg = "available in another assessment"
                        # else check if no one is in past without training mode
                        elif other_asse.filter(
                                start_time__lt=timezone.now(),
                                end_time__lte=timezone.now(),
                                training_time__gt=timezone.now()).exists():
                            do_access = False
                            do_see = False
                            err_msg = "not training mode"
                        # check if one asse is in training mode
                        elif not other_asse.filter(
                                start_time__lt=timezone.now(),
                                end_time__lt=timezone.now(),
                                training_time__lte=timezone.now()).exists():
                            do_access = False
                            do_see = False
                            err_msg = "no past assessment"
                    else:
                        do_access = False
                        do_see = False
                        err_msg = "bad group or something"

                    # Test part
                    # print(f"[asse:{asse_item.id}][user:{curr_user.id}][ex2tst:{ex2tst_item.id}] : {err_msg}")
                    # test on exercise_details
                    info = f"asse:{asse_item.id}/user:{curr_user.id}/ex2tst:{ex2tst_item.id}"
                    with self.subTest(f"Ex.Details {info}"):
                        self.client.force_login(curr_user)
                        response = self.client.get(reverse('exercise_details'),
                                                   {"extest": ex2tst_item.id, "asse": asse_item.id})
                        if do_see:
                            self.assertEquals(response.status_code, 200)
                        else:
                            self.assertIn("controller_error_message", response.context.keys())
                    # test on exercise_write
                    with self.subTest(f"Ex.Write   {info}"):
                        self.client.force_login(curr_user)
                        response = self.client.get(reverse('exercise_write'),
                                                   {"extest": ex2tst_item.id, "asse": asse_item.id})
                        if do_access:
                            self.assertEquals(response.status_code, 200)
                        else:
                            self.assertIn("controller_error_message", response.context.keys())
                    for lang in Language.objects.all():
                        lang_access = True
                        if not ex2tst_item.exotest2lang_set.filter(lang__name=lang.name).exists():
                            lang_access = False
                        # test on exercise_inspect
                        with self.subTest(f"Ex.Inspect {info}/lang{lang.id}:{lang.name}"):
                            request = self.factory.post(reverse('exercise_inspect'),
                                                        {
                                                            "ex2tst_id": ex2tst_item.id,
                                                            "asse_id": asse_item.id,
                                                            "lang_id": lang.id,
                                                            "raw_code": lang.default_code})
                            request.user = curr_user
                            response = ctrl_json_exercise_inspect(request)
                            dict_json = json.loads(response.content)
                            if do_access and lang_access:
                                if lang.name in self.lang:
                                    self.assertEquals(dict_json["err_msg"], "")
                                else:
                                    self.assertEquals(dict_json["exit_code"], ERROR_CODE_UNSUPPORTED)
                            else:
                                self.assertNotEquals(dict_json["err_msg"], "")

                        # test on exercise_stats_get
                        with self.subTest(f"Ex.Stat_get {info}/lang{lang.id}:{lang.name}"):
                            request = self.factory.post(reverse('exercise_stats_get'),
                                                        {
                                                            "ex2tst_id": ex2tst_item.id,
                                                            "asse_id": asse_item.id,
                                                            "lang_id": lang.id})
                            request.user = curr_user
                            response = ctrl_json_exercise_get_stat(request)
                            dict_json = json.loads(response.content)
                            if do_see and lang_access:
                                self.assertEquals(dict_json["err_msg"], "")
                            else:
                                self.assertNotEqual(dict_json["err_msg"], "")

    def test_OK(self):
        (user, extst, asse) = get_param_lang()
        for lang in Language.objects.all():
            info = f"[lang{lang.id}:{lang.name}]"

            if lang.name in self.lang:
                with open(os.path.join(".", "district", "tst_folder", "simple", "assets", lang.name, self.get_test_file(lang, self.CODE_TEST_OK)), "r") as f:
                    raw_code = f.read()

                request = self.factory.post(reverse('exercise_inspect'),
                                            {
                                                "ex2tst_id": extst.id,
                                                "asse_id": asse.id,
                                                "lang_id": lang.id,
                                                "raw_code": raw_code})
                request.user = user
                response = ctrl_json_exercise_inspect(request)
                dict_json = json.loads(response.content)
                with self.subTest(f"{info} error message"):
                    self.assertEquals(dict_json["err_msg"], "")
                with self.subTest(f"{info} percentage value"):
                    threshold = extst.solve_percentage_req
                    self.assertIn(dict_json["exit_code"], range(0, EX_INSPECT_ERROR_RANGE_MIN))
                    self.assertGreaterEqual(dict_json["exit_code"], threshold)
            else:
                with self.subTest(f"{info} language not supported"):
                    self.assertTrue(True)

    def test_NOK(self):
        (user, extst, asse) = get_param_lang()
        for lang in Language.objects.all():
            info = f"[lang{lang.id}:{lang.name}]"

            if lang.name in self.lang:
                with open(os.path.join(".", "district", "tst_folder", "simple", "assets", lang.name, self.get_test_file(lang, self.CODE_TEST_NOK)), "r") as f:
                    raw_code = f.read()

                request = self.factory.post(reverse('exercise_inspect'),
                                            {
                                                "ex2tst_id": extst.id,
                                                "asse_id": asse.id,
                                                "lang_id": lang.id,
                                                "raw_code": raw_code})
                request.user = user
                response = ctrl_json_exercise_inspect(request)
                dict_json = json.loads(response.content)
                with self.subTest(f"{info} error message"):
                    self.assertEquals(dict_json["err_msg"], "")
                with self.subTest(f"{info} percentage value"):
                    threshold = extst.solve_percentage_req
                    self.assertIn(dict_json["exit_code"], range(0, EX_INSPECT_ERROR_RANGE_MIN))
                    self.assertLess(dict_json["exit_code"], threshold)
            else:
                with self.subTest(f"{info} language not supported"):
                    self.assertTrue(True)

    def test_empty_code(self):
        (user, extst, asse) = get_param_lang()
        raw_code = ""
        for lang in Language.objects.all():
            info = f"[lang{lang.id}:{lang.name}]"

            if lang.name in self.lang:
                request = self.factory.post(reverse('exercise_inspect'),
                                            {
                                                "ex2tst_id": extst.id,
                                                "asse_id": asse.id,
                                                "lang_id": lang.id,
                                                "raw_code": raw_code})
                request.user = user
                response = ctrl_json_exercise_inspect(request)
                dict_json = json.loads(response.content)
                if self.lang_meta[lang.name]["is_compiled"]:
                    with self.subTest(f"{info} error message"):
                        self.assertEquals(dict_json["err_msg"], COMPILE_ERROR)
                    with self.subTest(f"{info} exit code"):
                        self.assertEquals(dict_json["exit_code"], ERROR_CODE_COMPILE)
                else:
                    with self.subTest(f"{info} error message"):
                        self.assertEquals(dict_json["err_msg"], "")
                    with self.subTest(f"{info} percentage value"):
                        threshold = extst.solve_percentage_req
                        self.assertIn(dict_json["exit_code"], range(0, EX_INSPECT_ERROR_RANGE_MIN))
                        self.assertLess(dict_json["exit_code"], threshold)
            else:
                with self.subTest(f"{info} language not supported"):
                    self.assertTrue(True)

    def test_syntax_error(self):
        (user, extst, asse) = get_param_lang()
        for lang in Language.objects.all():
            info = f"[lang{lang.id}:{lang.name}]"

            if lang.name in self.lang:
                with open(os.path.join(".", "district", "tst_folder", "simple", "assets", lang.name,
                                       self.get_test_file(lang, self.CODE_TEST_SYNTAX)), "r") as f:
                    raw_code = f.read()

                request = self.factory.post(reverse('exercise_inspect'),
                                            {
                                                "ex2tst_id": extst.id,
                                                "asse_id": asse.id,
                                                "lang_id": lang.id,
                                                "raw_code": raw_code})
                request.user = user
                response = ctrl_json_exercise_inspect(request)
                dict_json = json.loads(response.content)
                if self.lang_meta[lang.name]["is_compiled"]:
                    with self.subTest(f"{info} error message"):
                        self.assertEquals(dict_json["err_msg"], COMPILE_ERROR)
                    with self.subTest(f"{info} exit code"):
                        self.assertEquals(dict_json["exit_code"], ERROR_CODE_COMPILE)
                else:
                    with self.subTest(f"{info} error message"):
                        self.assertEquals(dict_json["err_msg"], "")
                    with self.subTest(f"{info} percentage value"):
                        threshold = extst.solve_percentage_req
                        self.assertIn(dict_json["exit_code"], range(0, EX_INSPECT_ERROR_RANGE_MIN))
                        self.assertLess(dict_json["exit_code"], threshold)
            else:
                with self.subTest(f"{info} language not supported"):
                    self.assertTrue(True)

    def test_infinite_loop(self):
        (user, extst, asse) = get_param_lang()
        for lang in Language.objects.all():
            info = f"[lang{lang.id}:{lang.name}]"

            if lang.name in self.lang:
                with open(os.path.join(".", "district", "tst_folder", "simple", "assets", lang.name, self.get_test_file(lang, self.CODE_TEST_INF_LOOP)), "r") as f:
                    raw_code = f.read()

                request = self.factory.post(reverse('exercise_inspect'),
                                            {
                                                "ex2tst_id": extst.id,
                                                "asse_id": asse.id,
                                                "lang_id": lang.id,
                                                "raw_code": raw_code})
                request.user = user
                response = ctrl_json_exercise_inspect(request)
                dict_json = json.loads(response.content)
                print(dict_json)
                with self.subTest(f"{info} error message"):
                    self.assertEquals(dict_json["err_msg"], "")
                with self.subTest(f"{info} exit code"):
                    self.assertEquals(dict_json["exit_code"], ERROR_CODE_TIMEOUT)
            else:
                with self.subTest(f"{info} language not supported"):
                    self.assertTrue(True)

    def test_code_too_long(self):
        (user, extst, asse) = get_param_lang()
        for lang in Language.objects.all():
            info = f"[lang{lang.id}:{lang.name}]"

            if lang.name in self.lang:
                # at the limit size
                with open(os.path.join(".", "district", "tst_folder", "simple", "assets", lang.name,
                                       self.get_test_file(lang, self.CODE_TEST_NOT_TOO_LONG)), "r") as f:
                    raw_code = f.read()

                request = self.factory.post(reverse('exercise_inspect'),
                                            {
                                                "ex2tst_id": extst.id,
                                                "asse_id": asse.id,
                                                "lang_id": lang.id,
                                                "raw_code": raw_code})
                request.user = user
                response = ctrl_json_exercise_inspect(request)
                dict_json = json.loads(response.content)
                with self.subTest(f"{info} error message"):
                    self.assertEquals(dict_json["err_msg"], "")
                with self.subTest(f"{info} percentage value"):
                    self.assertEquals(dict_json["exit_code"], EX_INSPECT_ERROR_RANGE_MIN-1)

                # beyond the limit size
                with open(os.path.join(".", "district", "tst_folder", "simple", "assets", lang.name,
                                       self.get_test_file(lang, self.CODE_TEST_TOO_LONG)), "r") as f:
                    raw_code = f.read()

                request = self.factory.post(reverse('exercise_inspect'),
                                            {
                                                "ex2tst_id": extst.id,
                                                "asse_id": asse.id,
                                                "lang_id": lang.id,
                                                "raw_code": raw_code})
                request.user = user
                response = ctrl_json_exercise_inspect(request)
                dict_json = json.loads(response.content)
                with self.subTest(f"{info} error message"):
                    self.assertNotEqual("err_msg", USER_RAW_CODE_TOO_BIG)
                with self.subTest(f"{info} percentage value"):
                    self.assertEquals(dict_json["exit_code"], ERROR_CODE_ACCESS)
            else:
                with self.subTest(f"{info} language not supported"):
                    self.assertTrue(True)

