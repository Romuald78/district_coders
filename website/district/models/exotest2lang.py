from django.db import models

from config.constants import default_value_cnf
from district.models.exo2test import Exo2Test
from district.models.language import Language


class ExoTest2Lang(models.Model):

    exo2test = models.ForeignKey(Exo2Test, on_delete=models.CASCADE)
    lang = models.ForeignKey(Language, on_delete=models.CASCADE)
    nb_test_try = models.IntegerField(default=0)
    nb_test_pass = models.IntegerField(default=0)
    nb_train_try = models.IntegerField(default=0)
    nb_train_pass = models.IntegerField(default=0)
    exec_timeout = models.IntegerField(default=default_value_cnf.TIMEOUT_DEFAULT_VALUE)
    exec_max_memory = models.IntegerField(default=-1)

    def __str__(self):
        out = f"ExoTest2Lang {self.exo2test}/lang:{self.lang}"
        return out
