import subprocess

from toolbox.exercise_generation.user_program import UserProgram
from website.settings import MEDIA_ROOT

import os


class CProgram(UserProgram):
    def __init__(self, raw_code, user_id):
        super().__init__()
        self.raw_code = raw_code
        self.user_id = user_id
        self.filepath = os.path.join(MEDIA_ROOT, "user_codes", f"code_{user_id}", f"user_{user_id}.c")
        self.exec_cmd = os.path.join(MEDIA_ROOT, "user_codes", f"code_{user_id}", f"user_{user_id}.exe")
        # store the raw code into the user file
        UserProgram.create_user_file(self.filepath, self.raw_code)

    # TODO Remove this useless method ????
    def get_filepath(self):
        return self.filepath

    def get_exec_cmd(self):
        return self.exec_cmd

    def compile(self, gen_file=""):
        if len(gen_file) == 0:
            result = subprocess.run(["gcc", self.filepath, "-o", self.exec_cmd], capture_output=True)
        else:
            print("gen file", gen_file)
            exit()
            # Retrieve the verification exec file path
            ex_corr_c = os.path.join(MEDIA_ROOT, "exercises", "mode_include", f"{gen_file}.c")
            bin_dir = os.path.join(MEDIA_ROOT, "exercises", "bin")
            ldc_dir = os.path.join(MEDIA_ROOT, "exercises", "libDC")

            # compile in one file
            result = subprocess.run(["gcc", self.filepath, ex_corr_c, f"-L{bin_dir}", "-lDC", f"-I{ldc_dir}", "-o", self.exec_cmd], capture_output=True)

        return (result.returncode, result.stdout, result.stderr)

    def __str__(self):
        return f"raw code: {self.raw_code}"
