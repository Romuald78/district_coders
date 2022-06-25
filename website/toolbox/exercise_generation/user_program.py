import os.path

from toolbox.utils.utils import recreate_dir


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
        # (re)create dirname
        recreate_dir(dirname)
        # create .exe file
        with open(filepath, 'w', encoding="UTF-8") as f:
            f.write(raw_code)

    def compile(self, genfile, insp_mode):
        raise Exception(f"'{self.compile.__name__}' method has not been implemented yet in {self}")