
#----------------------------------------------
import os.path
from datetime import timedelta

from django.utils import timezone

from district.models.assessment import Assessment
from district.models.exercise import Exercise
from district.models.exo2test import Exo2Test
from district.models.exotest2lang import ExoTest2Lang
from district.models.group import GroupDC
from district.models.inspector_mode import InspectorMode
from district.models.language import Language
from district.models.test import TestDC
from district.models.testresult import TestResult
from district.models.user import UserDC
from config.secure.admin_cnf import ADMIN_EMAIL
from website.settings import DEBUG, DEFAULT_GROUP_KEY

def createAdmin():
    # create admin user
    admin = UserDC()
    admin.username = "admin"
    admin.is_superuser = True
    admin.is_staff = True
    admin.is_active = True
    admin.set_password("admin")
    admin.email = ADMIN_EMAIL
    admin.save()
    #print(f"    > Admin [{admin.id}]:'{admin.username}' added !")

def createExercises():
    exercises = []
    for i in range(15):
        letter = chr(65+i)
        stdio = InspectorMode.objects.all().filter(name__icontains="stdio")
        obj = Exercise()
        obj.title = f"Exercise {letter}"
        obj.description = f"Exercise #{letter} for debug purpose only (absolute value)"
        obj.gen_file = os.path.join("debug", f"ex_debug_{letter}")
        obj.insp_mode = stdio.first()
        obj.save()
        exercises.append(obj)
        #print(f"    > Exercise [{obj.id}]:'{obj.title}' added !")
    return exercises

def createTests():
    tests = []
    for num in "12345678":
        name = f"Test_#{num}"
        desc = f"Test #{num} that contains some exercices"
        obj = TestDC()
        obj.title = name
        obj.description = desc
        obj.save()
        tests.append(obj)
        #print(f"    > Test [{obj.id}]:'{obj.title}' added !")
    return tests

EX2TST = [
    [1,5,8,10,12,13,14,15],
    [2,5,6,9,11,13,14,15],
    [3,6,7,10,11,12,14,15],
    [4,7,8,9,11,12,13,15],
    [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15],
    [1,2,3],
    [1,2,3,4],
    [15],
]
EX2TST_SOLVE_PER_REQ = [
    [100.0,100.0,100.0,100.0,100.0,100.0,100.0,100.0],
    [100.0,100.0,100.0,100.0,100.0,100.0,100.0,100.0],
    [100.0,100.0,100.0,100.0,100.0,100.0,100.0,100.0],
    [100.0,100.0,100.0,100.0,100.0,100.0,100.0,100.0],
    [100.0,100.0,100.0,100.0,100.0,100.0,100.0,100.0,100.0,100.0,100.0,100.0,100.0,100.0,100.0],
    [0.0,0.0,0.0],
    [100.0,0.0,50.0,0.0],
    [100.0],
]

def createExo2Test(exos, tests):
    if len(tests) != len(EX2TST):
        print(f"    > ERROR : bad lengths for test lists !")
        exit(1)
    if len(exos) != len(EX2TST[4]):
        print(f"    > ERROR : bad lengths for exo lists !")
        print(exos)
        print(EX2TST[-1])
        exit(2)
    if len(EX2TST_SOLVE_PER_REQ) != len(EX2TST):
        print(f"    > ERROR : bad lengths for EX2TST and EX2TST_SOLVE_PER_REQ lists !")
        exit(3)
    if [len(i) for i in EX2TST_SOLVE_PER_REQ] != [len(i) for i in EX2TST]:
        print(f"    > ERROR : bad lengths for EX2TST_SOLVE_PER_REQ lists !")
        exit(4)
    # for each tests
    exo2tests = []
    for t in range(len(EX2TST)):
        # init rank to 1
        rank = 1
        # for each exercise in the test
        for i in range(len(EX2TST[t])):
            e = EX2TST[t][i]
            obj = Exo2Test()
            obj.test = tests[t]
            obj.exercise = exos[e - 1]
            obj.rank = rank
            obj.score = rank
            obj.solve_percentage_req = EX2TST_SOLVE_PER_REQ[t][i]
            rank += 1
            obj.save()
#            print(f"    > Exo2Test [{obj.id}]: test #{t+1} -> exo #{e} added !")
            exo2tests.append(obj)
    return exo2tests

def createExoTest2Lang(exo2tests):
    langs = [
        [1,2],
        [2,3],
        [3,4],
        [4,5],
        [5,6],
        [6,7],
        [1,3,5,7],
        [2,4,6],
        [1,3,4],
        [4,5,7],
        [3,4,5],
        [1,2,6,7],
        [2,3,4,5,6],
        [1,2,3,5,6,7],
        [1,2,3,4,5,6,7],
    ]
    # for each exo2test
    # find the exercise object and according to its ID,
    # link to the correct languages
    for e2t in exo2tests:
        ex_id = e2t.exercise.id - 1
        lang_list = langs[ex_id]
        for lang_id in lang_list:
            obj = ExoTest2Lang()
            obj.nb_test_try     = 0
            obj.nb_test_pass    = 0
            obj.nb_train_try    = 0
            obj.nb_train_pass   = 0
            # obj.exec_timeout    = -1
            obj.exec_max_memory = -1
            obj.exo2test     = e2t
            obj.lang_id            = lang_id
            obj.save()
#            print(f"    > ExoTest2Lang [{obj.id}]: ex2tst #{e2t.id} -> lang #{lang_id} added !")

def createGroups():
    for i in range(5):
        obj = GroupDC()
        obj.name = f"Group #{i+1}"
        obj.register_key = f"group{i+1}"
        obj.description = f"Group #{i+1} for all allowed users"
        obj.save()
#        print(f"    > Group [{obj.id}] added !")

# assessment data
ASSESS = [
    {"name": "Assessment T1",      "test_id": 1, "group": 1, "today": "training", "user_ex_done": []},
    {"name": "Assessment P1",      "test_id": 2, "group": 1, "today": "end"     , "user_ex_done": []},
    {"name": "Assessment P2",      "test_id": 2, "group": 2, "today": "end"     , "user_ex_done": []},
    {"name": "Assessment C2",      "test_id": 3, "group": 2, "today": "start"   , "user_ex_done": [(3, 3)]},
    {"name": "Assessment C3",      "test_id": 3, "group": 3, "today": "start"   , "user_ex_done": []},
    {"name": "Assessment F3",      "test_id": 4, "group": 3, "today": "future"  , "user_ex_done": []},
    {"name": "Assessment C3-done", "test_id": 4, "group": 3, "today": "start"   , "user_ex_done": [(3, ex_id) for ex_id in EX2TST[4-1]]},
    {"name": "Assessment T-all",   "test_id": 5, "group": 4, "today": "training", "user_ex_done": []},
    {"name": "Assessment P-all",   "test_id": 5, "group": 4, "today": "end"     , "user_ex_done": []},
    {"name": "Assessment C-all",   "test_id": 5, "group": 4, "today": "start"   , "user_ex_done": []},
    {"name": "Assessment F-all",   "test_id": 5, "group": 4, "today": "future"  , "user_ex_done": []},
    {"name": "Assessment C2-0%",   "test_id": 6, "group": 2, "today": "start"   , "user_ex_done": []},
    {"name": "Assessment C2-1050", "test_id": 7, "group": 2, "today": "start"   , "user_ex_done": [(3, 1)]},
    {"name": "Assessment C2-ex15", "test_id": 8, "group": 2, "today": "start"   , "user_ex_done": []},
]
def createAssess(tests):
    # Get current date and month delta
    month = timedelta(days=30)
    today = timezone.now()
    # Compute month shifted dates
    m2 = today - month * 2
    m1 = today - month
    p1 = today + month
    p2 = today + month * 2
    p3 = today + month * 3
    # now create all assessments according to the array data
    for assess in ASSESS:
        # Get assessment information
        test_id = assess["test_id"]
        grp_id = assess["group"] + 1  # +1 because of the default 'everyone' group
        name = assess["name"]
        x_time = assess["today"]
        # Init object
        obj = Assessment()
        obj.start_time    = 0
        obj.end_time      = 0
        obj.training_time = 0
        obj.result_json   = ""
        obj.test_id          = test_id
        # apply dates according to test status
        if x_time == "training":
            obj.start_time = m2
            obj.end_time = m1
            obj.training_time = today
        elif x_time == "end":
            obj.start_time = m1
            obj.end_time = today
            obj.training_time = p1
        elif x_time == "start":
            obj.start_time = today
            obj.end_time = p1
            obj.training_time = p2
        elif x_time == "future":
            obj.start_time = p1
            obj.end_time = p2
            obj.training_time = p3
        else:
            print("[INTERNAL ERROR] !!!!")
            exit(3)
        # save object into
        obj.save()
        grp = GroupDC.objects.all().filter(id=grp_id).first()
        obj.groups.add(grp)
#        print(f"    > Assessment [{obj.id}]: test #{obj.test_id} added !")

def createUsers():
    groups = [
        "1","2","3","4",
        "12","13","14","23","24","34",
        "123","234","124","134",
        "1234"
    ]
    for grp_list in groups:
        name = f"user_{grp_list}"
        # create user here
        obj = UserDC()
        obj.username = name
        obj.is_superuser = False
        obj.is_staff = False
        obj.is_active = True
        obj.is_email_validated = True
        obj.set_password(f"pass_{grp_list}")
        obj.email = f"{name}@dummy.com"
        obj.save()
        # Add this user to all the groups in the list
        for grp in grp_list:
            search_id = int(grp)+1
            grp = GroupDC.objects.all().filter(id=search_id).first()
            obj.groups.add(grp)
        # Add to default group
        def_grp = GroupDC.objects.filter(register_key=DEFAULT_GROUP_KEY)
        obj.groups.add(def_grp.first())


#        print(f"    > User [{obj.id}]:'{obj.username}' added !")

def createTestResult():
    lang_available = ["C", "JS", "PHP"]

    for i in range(len(ASSESS)):
        asse = Assessment.objects.get(id=i+1)
        for (user_id, ex_id) in ASSESS[i]["user_ex_done"]:
            search_valid_lang = True
            ex2tst = Exo2Test.objects.get(test_id=asse.test.id, exercise=ex_id)
            user = UserDC.objects.get(id=user_id)
            for language in lang_available:
                if search_valid_lang:
                    extst2lang = ex2tst.exotest2lang_set.filter(lang__name=language)
                    if len(extst2lang.all()) > 0:
                        search_valid_lang = False
                        TestResult.objects.create(
                            exo_test2lang=extst2lang.first(),
                            user=user,
                            solve_code=extst2lang.first().lang.default_code,
                            solve_percentage=100,
                            assessment_id=i+1)

def debug_migration():
    # Only process this migration if we are in a debug session
    # In production, it is useless to do it
    if not DEBUG:
        return
    # Create 15 exercises
    exos = createExercises()
    # Create 5 tests
    tests = createTests()
    # Create links between exos and tests
    exo2tests = createExo2Test(exos, tests)
    # Create links with languages
    createExoTest2Lang(exo2tests)
    # create groups
    createGroups()
    # Now create assessments to tests
    createAssess(tests)
    # Now create users with groups
    createUsers()
    # Now create test results
    createTestResult()
