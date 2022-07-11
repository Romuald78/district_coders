import json
import os.path
from datetime import timedelta

from django.core import management
from django.test import TransactionTestCase, RequestFactory
from django.urls import reverse
from django.utils import timezone

from district.controllers.ctrl_exercise import ctrl_json_exercise_inspect, ctrl_exercise_details, ctrl_exercise_write
from district.models.assessment import Assessment
from district.models.exo2test import Exo2Test
from district.models.exotest2lang import ExoTest2Lang
from district.models.group import GroupDC
from district.models.language import Language
from district.models.test import TestDC
from district.models.testresult import TestResult
from district.models.user import UserDC
from website.settings import MEDIA_ROOT


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

        # solve an exercise to see the behavior
        user = UserDC.objects.get(username="user_2")
        exotst2lang = ExoTest2Lang.objects.get(exo2test_id=17, lang__name="JS")
        TestResult.objects.create(
            exo_test2lang=exotst2lang,
            user=user,
            solve_code=exotst2lang.lang.default_code,
            solve_percentage=100,
            assessment_id=4)

        # create an assessment, and solve it totally
        month = timedelta(days=30)
        today = timezone.now()
        my_test = TestDC.objects.get(title="Test_#4")
        my_asse = Assessment.objects.create(
            start_time=today - month,
            end_time=today + month,
            training_time=today + month * 2,
            test_id=my_test.id
        )

        my_group = GroupDC.objects.get(name="Group #2")
        my_asse.groups.add(my_group)

        for ex2tst in my_test.exo2test_set.all():
            search_valid_lang = True
            for language in self.lang:
                if search_valid_lang:
                    extst2lang = ex2tst.exotest2lang_set.filter(lang__name=language)
                    if len(extst2lang.all()) > 0:
                        search_valid_lang = False
                        TestResult.objects.create(
                            exo_test2lang=extst2lang.first(),
                            user=user,
                            solve_code=exotst2lang.lang.default_code,
                            solve_percentage=100,
                            assessment_id=my_asse.id)

    # python manage.py test district.tst_folder.simple.test_exercise_inspector.ExerciseInspectorTest.test_user_access -v 2 --failfast
    def test_user_access(self):
        for asse_item in Assessment.objects.all():
            # check the rank
            # getting max rank of complete exercise
            min_rank_todo = asse_item.test.exo2test_set.order_by("rank").first().rank
            min_search = True
            is_test_complete = True
            for asse_ex2tst in asse_item.test.exo2test_set.order_by("-rank"):
                if min_search:
                    extst2lng_all = asse_ex2tst.exotest2lang_set.order_by("-testresult__solve_percentage")
                    if len(extst2lng_all.all()) > 0:
                        extst2lng = extst2lng_all.first()
                        if len(extst2lng.testresult_set.all()) == 0 \
                                or extst2lng.testresult_set.first().solve_percentage < asse_ex2tst.solve_percentage_req:
                            is_test_complete = False
                            min_rank_todo = asse_ex2tst.rank
                        else:
                            min_search = False
            for ex2tst_item in Exo2Test.objects.all():
                for curr_user in UserDC.objects.all():
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
                                if ex2tst_item.rank != min_rank_todo or is_test_complete:
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
                    # print(f"[asse:{asse_item.id}][ex2tst:{ex2tst_item.id}][user:{curr_user.id}] : {err_msg}")
                    # test on exercise_details
                    with self.subTest():
                        request = self.factory.get(reverse('exercise_details'),
                                                   {"extest": ex2tst_item.id, "asse": asse_item.id})
                        request.user = curr_user
                        response = ctrl_exercise_details(request)
                        if do_see:
                            self.assertEqual(response.status_code, 200)
                        else:
                            self.assertEqual(response.status_code, 302)
                    # test on exercise_write
                    with self.subTest():
                        request = self.factory.get(reverse('exercise_write'),
                                                   {"extest": ex2tst_item.id, "asse": asse_item.id})
                        request.user = curr_user
                        response = ctrl_exercise_write(request)
                        if do_access:
                            self.assertEqual(response.status_code, 200)
                        else:
                            self.assertEqual(response.status_code, 302)
                    # test on exercise_inspect
                    with self.subTest():
                        for lang in Language.objects.filter(name__in=self.lang).all():
                            lang_access = True
                            if len(ex2tst_item.exotest2lang_set.filter(lang__name=lang.name).all()) == 0:
                                lang_access = False
                            # print(f"--> {lang.name}")
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
                                self.assertNotIn("err_msg", dict_json)
                            else:
                                self.assertIn("err_msg", dict_json)

    # TODO only works for C script
    def test_OK(self):
        # getting the user
        user = UserDC.objects.get(username="user_4")
        extst = Exo2Test.objects.get(id=33)
        asse = Assessment.objects.get(id=9)
        lang = Language.objects.get(name="C")
        with open(os.path.join(MEDIA_ROOT, "..", "..", "tmp", "user001.c"), "r") as f:
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
            self.assertNotIn("err_msg", dict_json)
        with self.subTest():
            self.assertEqual(dict_json["exit_code"], 0)

    def test_NOK(self):
        # getting the user
        user = UserDC.objects.get(username="user_4")
        extst = Exo2Test.objects.get(id=33)
        asse = Assessment.objects.get(id=9)
        lang = Language.objects.get(name="C")
        with open(os.path.join(MEDIA_ROOT, "..", "..", "tmp", "user001 - wrong.c"), "r") as f:
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
            self.assertNotIn("err_msg", dict_json)
        with self.subTest():
            self.assertEqual(dict_json["exit_code"], 1)

    def test_empty_code(self):
        # getting the user
        user = UserDC.objects.get(username="user_4")
        extst = Exo2Test.objects.get(id=33)
        asse = Assessment.objects.get(id=9)
        lang = Language.objects.get(name="C")
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
        with self.subTest():
            self.assertNotIn("err_msg", dict_json)
        with self.subTest():
            self.assertEqual(dict_json["exit_code"], 1)

    def test_syntax_error(self):
        # getting the user
        user = UserDC.objects.get(username="user_4")
        extst = Exo2Test.objects.get(id=33)
        asse = Assessment.objects.get(id=9)
        lang = Language.objects.get(name="C")
        with open(os.path.join(MEDIA_ROOT, "..", "..", "tmp", "user001 - syntax.c"), "r") as f:
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
            self.assertNotIn("err_msg", dict_json)
        with self.subTest():
            self.assertEqual(dict_json["exit_code"], 1)

    def test_infinite_loop(self):
        # getting the user
        user = UserDC.objects.get(username="user_4")
        extst = Exo2Test.objects.get(id=33)
        asse = Assessment.objects.get(id=9)
        lang = Language.objects.get(name="C")
        with open(os.path.join(MEDIA_ROOT, "..", "..", "tmp", "user001 - infLoop.c"), "r") as f:
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
            self.assertNotIn("err_msg", dict_json)
        with self.subTest():
            self.assertEqual(dict_json["exit_code"], 1)

    def test_code_too_long(self):
        # getting the user
        user = UserDC.objects.get(username="user_4")
        extst = Exo2Test.objects.get(id=33)
        asse = Assessment.objects.get(id=9)
        lang = Language.objects.get(name="C")

        # at the limit size
        with open(os.path.join(MEDIA_ROOT, "..", "..", "tmp", "user001 - almostTooLong.c"), "r") as f:
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
            self.assertNotIn("err_msg", dict_json)
        with self.subTest():
            self.assertEqual(dict_json["exit_code"], 0)

        # beyond the limit size
        with open(os.path.join(MEDIA_ROOT, "..", "..", "tmp", "user001 - tooLong.c"), "r") as f:
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
            self.assertIn("err_msg", dict_json)
        with self.subTest():
            self.assertEqual(dict_json["exit_code"], 3)
