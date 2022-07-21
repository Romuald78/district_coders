from district.models.testresult import TestResult


# param :
#     int user_id
#     int asse_id
#     List of ExoTest2Lang ex_tst_lng_objs
# return :
#     List of dict of {
#         TestResult testresult_obj
#         Language lang_obj
#     }
def get_testresult(user_id, asse_id, ex_tst_lng_objs):

    all_testresult = []
    for ex_tst_lng in ex_tst_lng_objs:
        testresult = TestResult.objects.filter(user_id=user_id, assessment_id=asse_id, exo_test2lang_id=ex_tst_lng)
        if testresult.exists():
            all_testresult.append({"testresult_obj": testresult.first(), "lang_obj": ex_tst_lng.lang})

    return all_testresult
