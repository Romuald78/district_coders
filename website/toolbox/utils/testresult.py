from district.models.testresult import TestResult


# param :
#     int user_id
#     int asse_id
#     List of ExoTest2Lang ex_tst_lng_objs
# return :
#     List of dict of {
#         int exit_code
#             4: testresult not found
#         TestResult testresult
#     }
def get_testresult(user_id, asse_id, ex_tst_lng_objs):

    all_testresult = []
    for ex_tst_lng in ex_tst_lng_objs:
        testresult = TestResult.objects.filter(user_id=user_id, assessment_id=asse_id, exo_test2lang_id=ex_tst_lng)
        if len(testresult.all()) != 0:
            all_testresult.append({"testresult_obj": testresult.first(), "lang_obj": ex_tst_lng.lang_id})

    return all_testresult
