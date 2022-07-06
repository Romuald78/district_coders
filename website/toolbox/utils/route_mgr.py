from config.constants.route_cnf import PAGES

class Page():

    def __init__(self, name, url, ctrl, type="view", log_req=True):
        self.name = name
        self.url = url
        self.ctrl = ctrl
        self.type = type
        self.log_req= log_req



class PageManager():

    def __checkName(self, name):
        if name not in self.pages:
            raise Exception(f"Page Name error ! {page}")

    def __init__(self):
        self.pages = {}
        for page in PAGES:
            if page.name in self.pages:
                raise Exception(f"Page already added ! {page}")
            self.pages[page.name] = page

    def getPage(self, name):
        self.__checkName(name)
        return self.pages[name]

    def isView(self, name):
        page = self.getPage(name)
        return page.type == "view"

    def isJson(self, name):
        page = self.getPage(name)
        return page.type == "json"

    def getType(self, name):
        page = self.getPage(name)
        return page.type

    def getURL(self, name):
        page = self.getPage(name)
        return page.url

    def getController(self, name):
        page = self.getPage(name)
        return page.ctrl

    def login_required(self, name):
        page = self.getPage(name)
        return page.log_req
