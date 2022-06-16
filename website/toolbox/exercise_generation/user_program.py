import os.path
from shutil import rmtree


class UserProgram():
    def __init__(self):
        pass

    def get_filepath(self):
        raise Exception(f"'{self.get_filepath.__name__}' method has not been implemented yet in {self}")

    def get_exec_cmd(self):
        raise Exception(f"'{self.get_exec_cmd().__name__}' method has not been implemented yet in {self}")

    @staticmethod
    def create_user_file(filepath, raw_code):
        dirname = os.path.dirname(filepath)
        # if directory exists -> delete it
        if os.path.exists(dirname):
            rmtree(dirname)
        # create directory
        os.makedirs(dirname)
        # create .exe file
        with open(filepath, 'w', encoding="UTF-8") as f:
            f.write(raw_code)

    def compile(self):
        raise Exception(f"'{self.compile.__name__}' method has not been implemented yet in {self}")