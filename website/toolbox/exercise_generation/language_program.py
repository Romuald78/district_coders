import subprocess

from config.constants.error_message_cnf import ERROR_CODE_OK
from config.constants.exec_paths_cnf import PYTHON_EXEC, GCC_EXEC, PHP_EXEC, JS_EXEC, JAVAC_EXEC, JAVA_EXEC
from config.constants.inspector_mode_cnf import INSPECTOR_MODE_STDIO, INSPECTOR_MODE_INCLUDE
from toolbox.exercise_generation.user_program import UserProgram
from website.settings import MEDIA_ROOT

import os


class JAVAProgram(UserProgram):

    def __init__(self, raw_code, user_id):
        super().__init__()
        self.raw_code = raw_code
        self.user_id = user_id

        self.filepath = os.path.join(MEDIA_ROOT, "user_codes", f"code_{user_id}", f"User.java")
        classpath     = os.path.join(MEDIA_ROOT, "user_codes", f"code_{user_id}", f"User")
        self.exec_cmd = [JAVA_EXEC, classpath]
        # store the raw code into the user file
        UserProgram.create_user_file(self.filepath, self.raw_code)

    def get_exec_cmd(self):
        return self.exec_cmd

    def compile(self, gen_file, insp_mode):
        if insp_mode == INSPECTOR_MODE_STDIO:
            result = subprocess.run([JAVAC_EXEC, self.filepath], capture_output=True)
        else:
            raise Exception("JavaProgram compilation not implemented. (mode include)")

        return (result.returncode, result.stdout, result.stderr)



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
        return [self.exec_cmd,]

    def compile(self, gen_file, insp_mode):
        if insp_mode == INSPECTOR_MODE_STDIO:
            result = subprocess.run([GCC_EXEC, self.filepath, "-o", self.exec_cmd], capture_output=True)
        elif insp_mode == INSPECTOR_MODE_INCLUDE:
            # Retrieve the verification exec file path
            ex_corr_c = os.path.join(MEDIA_ROOT, "exercises", "mode_include", f"{gen_file}.c")
            bin_dir = os.path.join(MEDIA_ROOT, "exercises", "bin")
            ldc_dir = os.path.join(MEDIA_ROOT, "exercises", "libDC")

            # compile in one file
            result = subprocess.run([GCC_EXEC, self.filepath, ex_corr_c, f"-L{bin_dir}", "-lDC", f"-I{ldc_dir}", "-o", self.exec_cmd], capture_output=True)
        else:
            raise Exception(f"Bad inspector mode value {insp_mode}")
        return (result.returncode, result.stdout, result.stderr)

    def __str__(self):
        return f"raw code: {self.raw_code}"


class PYTHONProgram(UserProgram):
    def __init__(self, raw_code, user_id):
        super().__init__()
        self.raw_code = raw_code
        self.user_id = user_id
        self.filepath = os.path.join(MEDIA_ROOT, "user_codes", f"code_{user_id}", f"user_{user_id}.py")
        self.exec_cmd = [PYTHON_EXEC, self.filepath]
        # store the raw code into the user file
        UserProgram.create_user_file(self.filepath, self.raw_code)

    # TODO Remove this useless method ????
    def get_filepath(self):
        return self.filepath

    def get_exec_cmd(self):
        return self.exec_cmd

    def compile(self, gen_file, insp_mode):
        return (ERROR_CODE_OK, "".encode("UTF-8"), "".encode("UTF-8"))

    def __str__(self):
        return f"raw code: {self.raw_code}"


class PHPProgram(UserProgram):
    def __init__(self, raw_code, user_id):
        super().__init__()
        self.raw_code = raw_code
        self.user_id = user_id
        self.filepath = os.path.join(MEDIA_ROOT, "user_codes", f"code_{user_id}", f"user_{user_id}.php")
        self.exec_cmd = [PHP_EXEC, self.filepath]
        # store the raw code into the user file
        UserProgram.create_user_file(self.filepath, self.raw_code)

    # TODO Remove this useless method ????
    def get_filepath(self):
        return self.filepath

    def get_exec_cmd(self):
        return self.exec_cmd

    def compile(self, gen_file, insp_mode):
        return (ERROR_CODE_OK, "".encode("UTF-8"), "".encode("UTF-8"))

    def __str__(self):
        return f"raw code: {self.raw_code}"

class JSProgram(UserProgram):
    def __init__(self, raw_code, user_id):
        super().__init__()
        self.raw_code = raw_code
        self.user_id = user_id
        self.filepath = os.path.join(MEDIA_ROOT, "user_codes", f"code_{user_id}", f"user_{user_id}.js")
        self.exec_cmd = [JS_EXEC, self.filepath]
        # store the raw code into the user file

        file = open(os.path.join(MEDIA_ROOT, "exercises", "libDC", "header.js.inc"))
        header = file.read()
        file = open(os.path.join(MEDIA_ROOT, "exercises", "libDC", "footer.js.inc"))
        footer = file.read()
        file.close()
        UserProgram.create_user_file(self.filepath, header + self.raw_code + footer)

    # TODO Remove this useless method ????
    def get_filepath(self):
        return self.filepath

    def get_exec_cmd(self):
        return self.exec_cmd

    def compile(self, gen_file, insp_mode):
        return (ERROR_CODE_OK, "".encode("UTF-8"), "".encode("UTF-8"))

    def __str__(self):
        return f"raw code: {self.raw_code}"
