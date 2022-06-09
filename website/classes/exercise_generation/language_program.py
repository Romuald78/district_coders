import subprocess

from classes.exercise_generation.user_program import UserProgram
from website.settings import MEDIA_ROOT

import os


class CProgram(UserProgram):
    def __init__(self, raw_code, user_id):
        super().__init__()
        self.raw_code = raw_code
        self.user_id = user_id
        self.filepath = os.path.join(MEDIA_ROOT, "user_codes", f"{user_id}.c")
        self.exec_cmd = os.path.join(MEDIA_ROOT, "user_codes", f"{user_id}.exe")
        # store the raw code into the user file
        UserProgram.create_user_file(self.filepath, self.raw_code)

    # TODO Remove this useless method ????
    # def get_filepath(self):
    #     return self.filepath

    def get_exec_cmd(self):
        return self.exec_cmd

    def compile(self):
        subprocess.run(["gcc", self.filepath, "-o", self.exec_cmd])

    def __str__(self):
        return f"raw code: {self.raw_code}"
