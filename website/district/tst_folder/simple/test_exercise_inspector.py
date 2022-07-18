import json
import os.path
from datetime import timedelta

from django.core import management
from django.test import TransactionTestCase, RequestFactory
from django.urls import reverse
from django.utils import timezone

from config.constants.default_value_cnf import EX_INSPECT_ERROR_RANGE_MIN
from config.constants.error_message_cnf import ERROR_CODE_OK, USER_RAW_CODE_TOO_BIG, ERROR_CODE_ACCESS, \
    ERROR_CODE_COMPILE, COMPILE_ERROR, ERROR_CODE_TIMEOUT
from district.controllers.ctrl_exercise import ctrl_json_exercise_inspect, ctrl_exercise_details, ctrl_exercise_write
from district.models.assessment import Assessment
from district.models.exo2test import Exo2Test
from district.models.language import Language
from district.models.user import UserDC


class ExerciseInspectorTest(TransactionTestCase):

    def __init__(self, methodName='test_user_access'):
        self.lang = ["C", "JS", "PHP"]
        super().__init__(methodName)

    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()
        # clear and populate the db
        management.call_command("dc_reinit")
        management.call_command("populate_multi")

    def get_param_lang(self, lang):
        if lang == "C":
            user = UserDC.objects.get(username="user_4")
            extst = Exo2Test.objects.get(id=33)
            asse = Assessment.objects.get(id=10)
            lang = Language.objects.get(name="C")
            return (user, extst, asse, lang)
        return None

    # python manage.py test district.tst_folder.simple.test_exercise_inspector.ExerciseInspectorTest.test_user_access -v 2 --failfast
    def test_user_access(self):

        # TEST PART
        for asse_item in Assessment.objects.all():
            for curr_user in UserDC.objects.all():
                rank_access = True
                for ex2tst_item in Exo2Test.objects.order_by("rank").all():
                    asse_qs = Assessment.objects.filter(test__exo2test=ex2tst_item, groups__userdc=curr_user, id=asse_item.id)
                    do_access = len(asse_qs.all()) > 0
                    do_see = len(asse_qs.all()) > 0
                    err_msg = "VALID"
                    if do_access:
                        other_asse = Assessment.objects.filter(test__exo2test=ex2tst_item, groups__userdc=curr_user)
                        # check if there are assessments in process
                        if len(other_asse.filter(start_time__lte=timezone.now(), end_time__gt=timezone.now()).all()) > 0:
                            # check if the current assessment is in process
                            if asse_item.start_time.__le__(timezone.now()) and asse_item.end_time.__gt__(timezone.now()):
                                if rank_access:
                                    # either solve_percentage_req = 0
                                    # either solver_percentage_req <= solve_percentage
                                    is_there_extstlng = len(ex2tst_item.exotest2lang_set.all()) > 0
                                    if is_there_extstlng:
                                        test_result_not_nul = ex2tst_item.exotest2lang_set.order_by("-testresult__solve_percentage").first()
                                        is_there_testresult = len(test_result_not_nul.testresult_set.all()) > 0
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
                                        #print("je passe ici")
                                        #print("A", ex2tst_item.solve_percentage_req == 0)
                                        #print("B", is_there_extstlng)
                                        #print("C", is_there_testresult)
                                        #print("D", is_solve_percentage_valid)
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
                        elif len(other_asse.filter(
                                start_time__lt=timezone.now(),
                                end_time__lte=timezone.now(),
                                training_time__gt=timezone.now()).all()) > 0:
                            do_access = False
                            do_see = False
                            err_msg = "not training mode"
                        # check if one asse is in training mode
                        elif not len(other_asse.filter(
                                start_time__lt=timezone.now(),
                                end_time__lt=timezone.now(),
                                training_time__lte=timezone.now()).all()) > 0:
                            do_access = False
                            do_see = False
                            err_msg = "no past assessment"
                    else:
                        do_access = False
                        do_see = False
                        err_msg = "bad group or something"

                    # Test part
                    #print(f"[asse:{asse_item.id}][user:{curr_user.id}][ex2tst:{ex2tst_item.id}] : {err_msg}")
                    # test on exercise_details
                    msg = f"asse:{asse_item.id}/user:{curr_user.id}/ex2tst:{ex2tst_item.id}"
                    with self.subTest(f"Ex.Details {msg}"):
                        request = self.factory.get(reverse('exercise_details'),
                                                   {"extest": ex2tst_item.id, "asse": asse_item.id})
                        request.user = curr_user
                        response = ctrl_exercise_details(request)
                        if do_see:
                            self.assertEqual(response.status_code, 200)
                        else:
                            self.assertEqual(response.status_code, 302)
                    # test on exercise_write
                    with self.subTest(f"Ex.Write   {msg}"):
                        request = self.factory.get(reverse('exercise_write'),
                                                   {"extest": ex2tst_item.id, "asse": asse_item.id})
                        request.user = curr_user
                        response = ctrl_exercise_write(request)
                        if do_access:
                            self.assertEqual(response.status_code, 200)
                        else:
                            self.assertEqual(response.status_code, 302)
                    # test on exercise_inspect
                    for lang in Language.objects.filter(name__in=self.lang).all():
                        with self.subTest(f"Ex.Inspect {msg}/lang{lang.id}:{lang.name}"):
                            lang_access = True
                            if len(ex2tst_item.exotest2lang_set.filter(lang__name=lang.name).all()) == 0:
                                lang_access = False
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
                                self.assertEqual(dict_json["err_msg"], "")
                            else:
                                self.assertNotEqual(dict_json["err_msg"], "")

    # TODO only works for C script
    def test_OK(self):
        (user, extst, asse, lang) = self.get_param_lang("C")

        with open(os.path.join(".", "district", "tst_folder", "simple", "assets", "user001.c"), "r") as f:
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
        with self.subTest("error message"):
            self.assertEqual(dict_json["err_msg"], "")
        with self.subTest("percentage value"):
            threshold = extst.solve_percentage_req
            self.assertIn(dict_json["exit_code"], range(0, EX_INSPECT_ERROR_RANGE_MIN))
            self.assertGreaterEqual(dict_json["exit_code"], threshold)

    def test_NOK(self):
        (user, extst, asse, lang) = self.get_param_lang("C")

        with open(os.path.join(".", "district", "tst_folder", "simple", "assets", "user001 - wrong.c"), "r") as f:
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
        with self.subTest("error message"):
            self.assertEqual(dict_json["err_msg"], "")
        with self.subTest("percentage value"):
            # The user has answered the question
            threshold = extst.solve_percentage_req
            self.assertIn(dict_json["exit_code"], range(0,EX_INSPECT_ERROR_RANGE_MIN))
            self.assertLess(dict_json["exit_code"], threshold)

    def test_empty_code(self):
        (user, extst, asse, lang) = self.get_param_lang("C")
        raw_code = ""

        request = self.factory.post(reverse('exercise_inspect'),
                                    {
                                        "ex2tst_id": extst.id,
                                        "asse_id": asse.id,
                                        "lang_id": lang.id,
                                        "raw_code": raw_code})
        request.user = user
        response = ctrl_json_exercise_inspect(request)
        dict_json = json.loads(response.content)
        with self.subTest("error message"):
            self.assertEqual(dict_json["err_msg"], COMPILE_ERROR)
        with self.subTest("exit code"):
            self.assertEqual(dict_json["exit_code"], ERROR_CODE_COMPILE)

    def test_syntax_error(self):
        (user, extst, asse, lang) = self.get_param_lang("C")
        with open(os.path.join(".", "district", "tst_folder", "simple", "assets", "user001 - syntax.c"), "r") as f:
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
        with self.subTest("error message"):
            self.assertEqual(dict_json["err_msg"], COMPILE_ERROR)
        with self.subTest("exit code"):
            self.assertEqual(dict_json["exit_code"], ERROR_CODE_COMPILE)

    def test_infinite_loop(self):
        (user, extst, asse, lang) = self.get_param_lang("C")
        with open(os.path.join(".", "district", "tst_folder", "simple", "assets", "user001 - infLoop.c"), "r") as f:
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
        with self.subTest("error message"):
            self.assertEqual(dict_json["err_msg"], "")
        with self.subTest("exit code"):
            self.assertEqual(dict_json["exit_code"], ERROR_CODE_TIMEOUT)

    def test_code_too_long(self):
        (user, extst, asse, lang) = self.get_param_lang("C")

        # at the limit size
        with open(os.path.join(".", "district", "tst_folder", "simple", "assets", "user001 - almostTooLong.c"), "r") as f:
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
        with self.subTest():
            self.assertEqual(dict_json["err_msg"], "")
        with self.subTest():
            self.assertEqual(dict_json["exit_code"], EX_INSPECT_ERROR_RANGE_MIN-1)

        # beyond the limit size
        with open(os.path.join(".", "district", "tst_folder", "simple", "assets", "user001 - tooLong.c"), "r") as f:
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
        with self.subTest("error message"):
            self.assertNotEqual("err_msg", USER_RAW_CODE_TOO_BIG)
        with self.subTest("exit code"):
            self.assertEqual(dict_json["exit_code"], ERROR_CODE_ACCESS)
