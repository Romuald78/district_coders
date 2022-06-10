import os
import subprocess
from random import randint

from classes.constants import INSPECTOR_MODE_STDIO
from district.models.exercise import Exercise
from district.models.language import Language
import importlib

from website.settings import MEDIA_ROOT


class ExerciseInspector():

    def __init__(self, user_id, ex_id, lang_id, raw_code):
        self.user_id = user_id
        self.raw_code = raw_code
        self.ex_id = ex_id
        self.language = Language.objects.get(id=lang_id)
        module = importlib.import_module("classes.exercise_generation.language_program")
        class_ = getattr(module, self.language.language_program)
        self.program = class_(raw_code, user_id)

    def process(self):
        # retrieve exercise (+genFile)
        exercise = Exercise.objects.get(id=self.ex_id)

        # Get alea seed (XXXXX)
        seed = randint(0, 99999)
        seed = 123

        # Executable creation : either the user code only (mode STDIO) OR the exo+user code (mode INCLUDE)
        if exercise.insp_mode_id.name == INSPECTOR_MODE_STDIO:  # mode stdio #TODO use exercice object to retrieve mode
            # Compile user code if needed
            self.program.compile()
            # Retrieve the execution command string
            exec_cmd = self.program.get_exec_cmd()

            # Retrieve the verification exec file path
            ex_corr = os.path.join(MEDIA_ROOT, "exercises", "bin", exercise.gen_file)
            # Call the system
            # .../...../exo.exe -g -sXXXXX | execcommandstring | .../...../exo.exe -v -sXXXXX
            # print("commande : ", [ex_corr, "-g", f"-s{seed}", "|", exec_cmd, "|", ex_corr, "-v", f"-s{seed}"])
            part1 = subprocess.Popen([ex_corr, "-g", f"-s{seed}"], stdout=subprocess.PIPE)
            part2 = subprocess.Popen([exec_cmd], stdin=part1.stdout, stdout=subprocess.PIPE)
            part1.stdout.close()
            part3 = subprocess.Popen([ex_corr, "-v", f"-s{seed}"], stdin=part2.stdout, stdout=subprocess.PIPE)
            part2.stdout.close()
            result = part3.communicate()
            print("comm", result)

            # retrieve all return values (integer, stdout, stderr)
            # return all these info back to upper layer (dictionary ?)
            return (result.returncode, result.stdout, result.stderr)

        else:
            pass  # mode include #TODO
