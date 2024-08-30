class ideate:
    def __init__(self, title, abstract,success=True):
        self.title = title
        self.abstract = abstract
        self.success = success

    def __str__(self):
        return f"""Title:{self.title}\nAbstract:{self.abstract}"""

    def get_result(self):
        return self.title

    def get_rationale(self):
        return self.abstract

    def get_title(self):
        return self.title

    def get_abstract(self):
        return self.abstract

    @staticmethod
    def load_from_string(s):
        """
        s = Title:{self.title}\nAbstract:{self.abstract}
        """
        title = s.split("Title:")[1].split("Abstract:")[0].strip()
        abstract = s.split("Abstract:")[1].strip()
        return ideate(title, abstract)