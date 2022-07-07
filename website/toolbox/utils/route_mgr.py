import config.constants.route_cnf as route_cnf


class Page():

    def __init__(self, name, url, ctrl, type="view", log_req=True, parameters=False):
        self.name = name
        self.url = url
        self.ctrl = ctrl
        self.type = type
        self.log_req= log_req
        self.params = parameters

    def __str__(self):
        return "Page", self.name


class PageManager():

    def __check_name(self, name):
        if name not in self.pages:
            raise Exception(f"Page Name error ! {name}")

    def __init__(self):
        self.pages = {}
        for page in route_cnf.PAGES:
            if page.name in self.pages:
                raise Exception(f"Page already added ! {page}")
            self.pages[page.name] = page

    def get_page(self, name):
        self.__check_name(name)
        return self.pages[name]

    def is_view(self, name):
        page = self.get_page(name)
        return page.type == "view"

    def is_json(self, name):
        page = self.get_page(name)
        return page.type == "json"

    def get_type(self, name):
        page = self.get_page(name)
        return page.type

    def get_URL(self, name):
        page = self.get_page(name)
        return page.url

    def get_controller(self, name):
        page = self.get_page(name)
        return page.ctrl

    def is_login_required(self, name):
        page = self.get_page(name)
        return page.log_req

    def hasParameters(self, name):
        page = self.get_page(name)
        return page.params

    def get_pages(self):
        return self.pages

    def get_names(self):
        names = []
        for page in self.pages:
            names.append(page.name)
        return names