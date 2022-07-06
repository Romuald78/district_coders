


class Page():

    def __init__(self, name, url, ctrl, type="view", log_req=True):
        self.name = name
        self.url = url
        self.ctrl = ctrl
        self.type = type
        self.log_req= log_req


