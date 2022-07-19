import os
import subprocess
from random import randint

from config.constants import default_value_cnf, error_message_cnf
from config.constants.error_message_cnf import ERROR_CODE_OK, ERROR_CODE_ACCESS, ERROR_CODE_COMPILE, ERROR_CODE_TIMEOUT
from config.constants.inspector_mode_cnf import INSPECTOR_MODE_STDIO, INSPECTOR_MODE_INCLUDE
from district.models.exercise import Exercise
from district.models.language import Language
import importlib

from website.settings import MEDIA_ROOT


# TODO pour le mode include il faudra modifier la classe exec_inspect pour passer des parametres optionnels pour gerer les imports dynamiques
class ExerciseInspector():

    def __init__(self, user_id, ex_id, lang_id, raw_code, threshold, timeout):
        self.user_id = user_id
        self.raw_code = raw_code
        self.ex_id = ex_id
        self.language = Language.objects.get(id=lang_id)
        self.threshold = threshold
        self.timeout = timeout
        # if the string is overweighted (>1Mo)
        self.is_file_created = True
        if len(self.raw_code.encode("UTF-8")) > default_value_cnf.MAX_LENGTH_USER_RAW_CODE:
            self.is_file_created = False
        else:
            module = importlib.import_module("toolbox.exercise_generation.language_program")
            class_ = getattr(module, self.language.language_program)
            self.program = class_(raw_code, user_id)

    def process(self):
        if not self.is_file_created:
            return (ERROR_CODE_ACCESS, "", error_message_cnf.USER_RAW_CODE_TOO_BIG)
        # retrieve exercise (+genFile)
        exercise = Exercise.objects.get(id=self.ex_id) #TODO check the return of get
        # Get alea seed (XXXXX)
        seed = randint(0, 99999)
        # Retrieve the execution command string
        exec_cmd = self.program.get_exec_cmd()
        # Retrieve the verification exec file path
        ex_corr = os.path.join(MEDIA_ROOT, "exercises", "bin", f"{exercise.gen_file}.exe")

        # Compile user code if needed
        (exit_code_comp, stdout_comp, stderr_comp) = self.program.compile(exercise.gen_file, exercise.insp_mode.name)
        if exit_code_comp != ERROR_CODE_OK:
            return (ERROR_CODE_COMPILE, stdout_comp.decode("UTF-8"), stderr_comp.decode("UTF-8"))

        # Executable creation : either the user code only (mode STDIO) OR the exo+user code (mode INCLUDE)
        if exercise.insp_mode.name == INSPECTOR_MODE_STDIO:  # mode stdio
            # Call the system
            # .../...../exo.exe -g -sXXXXX -tYYYYY | execcommandstring | .../...../exo.exe -v -sXXXXX -tYYYYY
            part1 = subprocess.Popen([ex_corr, "-g", f"-s{seed}", f"-t{self.threshold}"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            part2 = subprocess.Popen(exec_cmd, stdin=part1.stdout, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            part3 = subprocess.Popen([ex_corr, "-v", f"-s{seed}", f"-t{self.threshold}"], stdin=part2.stdout, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            try:
                result = part3.communicate(timeout=self.timeout)
                exit_code_exec = part3.returncode
                part1.stdout.close()
                part2.stdout.close()
                part3.stdout.close()
                (stdout_exec, stderr_exec) = result
            except:
                part1.kill()
                part2.kill()
                part3.kill()
                result = part3.communicate()
                exit_code_exec = part3.returncode
                stdout_exec, stderr_exec = result
                if exit_code_exec == -9:  # killing code
                    exit_code_exec = ERROR_CODE_TIMEOUT
                    stdout_exec = "".encode("UTF-8")
                    stderr_exec = "Error timeout".encode("UTF-8")

        elif exercise.insp_mode.name == INSPECTOR_MODE_INCLUDE: # mode include
            # Call the system
            # .../...../exo.exe -g -sXXXXX | execcommandstring | .../...../exo.exe -v -sXXXXX
            # print("commande : ", [ex_corr, "-g", f"-s{seed}", "|", exec_cmd, "|", ex_corr, "-v", f"-s{seed}"])
            part1 = subprocess.Popen(exec_cmd + ["-g", f"-s{seed}"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            part2 = subprocess.Popen(exec_cmd + ["-v", f"-s{seed}"], stdin=part1.stdout, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            try:
                result = part2.communicate(timeout=self.timeout)
                exit_code_exec = part2.returncode
                part1.stdout.close()
                part2.stdout.close()
                (stdout_exec, stderr_exec) = result
            except:
                part1.kill()
                part2.kill()
                result = part2.communicate()
                exit_code_exec = part2.returncode
                # (stdout_exec, stderr_exec) = result
                stdout_exec = "".encode("UTF-8")
                stderr_exec = "Error timeout".encode("UTF-8")
        else:
            raise Exception(f"Bad inspector mode value {exercise.insp_mode.name}")

        # retrieve all return values (integer, stdout, stderr)
        # return all these info back to upper layer (dictionary ?)
        return (exit_code_exec, (stdout_comp + stdout_exec).decode("UTF-8"), (stderr_comp + stderr_exec).decode("UTF-8"))
