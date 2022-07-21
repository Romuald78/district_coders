from district.models.assessment import Assessment
from district.models.exo2test import Exo2Test
from district.models.user import UserDC


# current assessment with one exercise including every programming languages
def get_param_lang():
    user = UserDC.objects.get(username="user_2")
    extst = Exo2Test.objects.get(id=55)
    asse = Assessment.objects.get(id=14)
    return (user, extst, asse)