class Method:
    def __init__(self, scientificMethod, scientificMethodRationale, success=True):
        self.scientificMethod = scientificMethod
        self.scientificMethodRationale = scientificMethodRationale
        self.success = success

    def __str__(self):
        return f"""Method:{self.scientificMethod}\nRationale:{self.scientificMethodRationale}"""

    def get_result(self):
        return self.scientificMethod

    def get_rationale(self):
        return self.scientificMethodRationale

    @staticmethod
    def load_from_string(s):
        """
        s = f"Method:{self.scientificMethod}\nRationale:{self.scientificMethodRationale}"
        """
        scientificMethod = s.split("Rationale:")[0].split("Method:")[1]
        scientificMethodRationale =  s.split("Rationale:")[1]
        return Method(scientificMethod, scientificMethodRationale)
