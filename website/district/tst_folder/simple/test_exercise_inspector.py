from django.core import management
from django.db.models import Q
from django.test import TransactionTestCase, RequestFactory
from django.urls import reverse
from django.utils import timezone

from district.controllers.ctrl_exercise import ctrl_json_exercise_inspect, ctrl_exercise_details, ctrl_exercise_write
from district.models.assessment import Assessment
from district.models.exo2test import Exo2Test
from district.models.user import UserDC


class ExerciseInspectorTest(TransactionTestCase):
    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()
        # clear and populate the db
        management.call_command("dc_reinit")
        management.call_command("populate_multi")

    # python manage.py test district.tst_folder.simple.test_exercise_inspector.ExerciseInspectorTest.test_user_access -v 2 --failfast
    def test_user_access(self):
        for curr_user in UserDC.objects.all():
            for ex2tst_item in Exo2Test.objects.all():
                for asse_item in Assessment.objects.all():
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
                                # check the rank
                                # getting max rank of complete exercise
                                min_rank_todo = asse_item.test.exo2test_set.order_by("rank").first().rank
                                for asse_ex2tst in asse_item.test.exo2test_set.order_by("-rank"):
                                    extst2lng_all = asse_ex2tst.exotest2lang_set.order_by("-testresult__solve_percentage")
                                    if len(extst2lng_all.all()) > 0:
                                        extst2lng = extst2lng_all.first()
                                        if len(extst2lng.testresult_set.all()) > 0 \
                                                and extst2lng.testresult_set.first().solve_percentage < asse_ex2tst.solve_percentage_req:
                                            min_rank_todo = asse_ex2tst.rank
                                if ex2tst_item.rank != min_rank_todo:
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
                        # check if the current assessment is in training mode
                        # elif asse_item.start_time.__lt__(timezone.now()) and asse_item.end_time.__lt__(timezone.now()) and \
                        #         asse_item.training_time.__le__(timezone.now()):
                        #     do_access = False
                        #     err_msg = "only future assessment ?"
                    else:
                        do_access = False
                        do_see = False
                        err_msg = "bad group or something"

                    # Test part
                    # print(f"[user:{curr_user.id}][ex2tst:{ex2tst_item.id}][asse:{asse_item.id}] : {err_msg}")
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
                        for extst2lng in ex2tst_item.exotest2lang_set.filter(
                                lang__name__in=["C", "JS", "PHP"]).all():
                            lang = extst2lng.lang
                            # print(f"--> {lang.name}")
                            request = self.factory.post(reverse('exercise_inspect'),
                                                        {
                                                            "ex2tst_id": ex2tst_item.id,
                                                            "asse_id": asse_item.id,
                                                            "lang_id": lang.id,
                                                            "raw_code": lang.default_code})
                            request.user = curr_user
                            response = ctrl_json_exercise_inspect(request)
                            # TODO : read the json response (exit_code)
                            if do_access:
                                self.assertEqual(response.status_code, 200)
                            else:
                                self.assertEqual(response.status_code, 200)

    def test_OK(self):
        pass

    def test_NOK(self):
        pass

    def test_empty_code(self):
        pass

    def test_syntax_error(self):
        pass

    def test_infinite_loop(self):
        pass

    def test_code_too_long(self):
        pass
