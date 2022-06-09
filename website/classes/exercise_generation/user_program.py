class UserProgram():
    def __init__(self):
        pass

    def get_filepath(self):
        raise Exception(f"'{self.get_filepath.__name__}' method has not been implemented yet in {self}")

    def get_exec_cmd(self):
        raise Exception(f"'{self.get_exec_cmd().__name__}' method has not been implemented yet in {self}")

    @staticmethod
    def create_user_file(filepath, raw_code):
        with open(filepath, 'w', encoding="UTF-8") as f:
            f.write(raw_code)

    def compile(self):
        raise Exception(f"'{self.compile.__name__}' method has not been implemented yet in {self}")