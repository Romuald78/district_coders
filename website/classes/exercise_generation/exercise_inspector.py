from district.models.language import Language
import importlib


class ExerciseInspector():

    def __init__(self, user_id, ex_id, lang_id, raw_code):
        self.user_id = user_id
        self.raw_code = raw_code
        self.ex_id = ex_id
        print("hello")
        # self.language = Language.objects.get(id=lang_id)
        # module = importlib.import_module("language_program")
        # class_ = getattr(module, self.language.language_program)
        # self.program = class_(raw_code, user_id)

    def process(self):
        if True: # mode stdio
            self.program.compile()
        else:
            pass #mode include #TODO
