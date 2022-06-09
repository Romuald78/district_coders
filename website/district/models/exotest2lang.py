from django.db import models

from district.models.exo2test import Exo2Test
from district.models.language import Language


class ExoTest2Lang(models.Model):

    exo2test_id = models.ForeignKey(Exo2Test, on_delete=models.CASCADE)
    lang_id = models.ForeignKey(Language, on_delete=models.CASCADE)
    nb_test_try = models.IntegerField(default=0)
    nb_test_pass = models.IntegerField(default=0)
    nb_train_try = models.IntegerField(default=0)
    nb_train_pass = models.IntegerField(default=0)
    exec_timeout = models.IntegerField(default=-1)
    exec_max_memory = models.IntegerField(default=-1)

    def __str__(self):
        out = f"ExoTest2Lang {self.exo2test_id}/lang:{self.lang_id}"
        return out
