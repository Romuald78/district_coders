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

    def get_filepath(self):
        return self.filepath

    def get_exec_cmd(self):
        return self.exec_cmd

    def compile(self):
        subprocess.run(["gcc", self.filepath, "-o", f"{self.user_id}.exe"])
