from django.core import management
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

    def test_user_access(self):
        # on récup tous les user
        # on prend ses groupes->assessments, et tous les exos qui s'y trouvent
        # cet exo doit être soit dans un assessment en cours (et auquel cas dans le bon rank ...) soit dans un
        # assessment passé training

        # clear and populate the db
        management.call_command("dc_reinit")
        management.call_command("populate_multi")

        for user in UserDC.objects.all():
            for ex2tst in Exo2Test.objects.all():
                err_msg = "VALID"
                # access test by its groups
                asse_qs = Assessment.objects.filter(test__exo2test=ex2tst, groups__userdc=user)
                do_access = len(asse_qs.all()) > 0
                is_triable = True
                if do_access:
                    if len(asse_qs.filter(start_time__lte=timezone.now(), end_time__gt=timezone.now()).all()) > 0:
                        # check the rank
                        asse = asse_qs.filter(test__exo2test=ex2tst).first()
                        # getting max rank of complete exercise
                        min_rank_todo = asse.test.exo2test_set.order_by("rank").first().rank
                        for asse_ex2tst in asse.test.exo2test_set.order_by("-rank"):
                            extst2lng_all = asse_ex2tst.exotest2lang_set.order_by("-testresult__solve_percentage")
                            if len(extst2lng_all.all()) > 0:
                                extst2lng = extst2lng_all.first()
                                if len(extst2lng.testresult_set.all()) > 0 \
                                        and extst2lng.testresult_set.first().solve_percentage < asse_ex2tst.solve_percentage_req:
                                    min_rank_todo = asse_ex2tst.rank
                        if ex2tst.rank != min_rank_todo:
                            do_access = False
                            err_msg = "Rank not valid"
                    # else check if no one is in past without training mode
                    elif len(asse_qs.filter(
                            start_time__lt=timezone.now(),
                            end_time__lte=timezone.now(),
                            training_time__gt=timezone.now()).all()) > 0:
                        is_triable = False
                        do_access = False
                        err_msg = "not training mode"
                    # check if one asse is in process
                    elif not len(asse_qs.filter(
                            start_time__lt=timezone.now(),
                            end_time__lt=timezone.now(),
                            training_time__lte=timezone.now()).all()) > 0:
                        is_triable = False
                        do_access = False
                        err_msg = "no past assessment"
                    else:
                        is_triable = False
                        do_access = False
                        err_msg = "only future assessment ?"

                    if is_triable:
                        print(f"[user:{user.id}][ex2tst:{ex2tst.id}][asse:{asse.id}] : {err_msg}")
                        # test on exercise_details
                        with self.subTest():
                            request = self.factory.get(reverse('exercise_details'), {"extest": ex2tst.id, "asse": asse.id})
                            request.user = user
                            response = ctrl_exercise_details(request)
                            self.assertEqual(response.status_code, 200)
                        # test on exercise_write
                        with self.subTest():
                            request = self.factory.get(reverse('exercise_write'), {"extest": ex2tst.id, "asse": asse.id})
                            request.user = user
                            response = ctrl_exercise_write(request)
                            if do_access:
                                self.assertEqual(response.status_code, 200)
                            else:
                                self.assertEqual(response.status_code, 302)
                        # test on exercise_inspect
                        with self.subTest():
                            lang = ex2tst.exotest2lang_set.all().first().lang

                            request = self.factory.post(reverse('exercise_inspect'),
                                                        {
                                                            "ex2tst_id": ex2tst.id,
                                                            "asse_id": asse.id,
                                                            "lang_id": lang.id,
                                                            "raw_code": lang.default_code})
                            request.user = user
                            response = ctrl_json_exercise_inspect(request)
                            # TODO : read the json resonse (exit_code)
                            if do_access:
                                self.assertEqual(response.status_code, 200)
                            else:
                                self.assertEqual(response.status_code, 200)
                    else:
                        print(f"[user:{user.id}][ex2tst:{ex2tst.id}] : no assessment")
                else:
                    print(f"[user:{user.id}][ex2tst:{ex2tst.id}] : bad group")

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