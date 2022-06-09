from classes.exercise_generation.user_program import UserProgram


class CProgram(UserProgram):
    def __init__(self, raw_code):
        self.filepath = None
        self.exec_cmd = None
        self.raw_code = raw_code

    def get_filepath(self):
        return self.filepath

    def get_exec_cmd(self):
        return self.exec_cmd

    def create_user_file(self, filepath, raw_code):
        with open(filepath, 'w') as f:
            f.write(raw_code)