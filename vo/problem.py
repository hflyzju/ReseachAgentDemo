class Problem:
    def __init__(self, problem, rationale, success=True):
        self.problem = problem
        self.rationale = rationale
        self.success = success

    def __str__(self):
        return f"""Problem:{self.problem}\nRationale:{self.rationale}"""

    def get_result(self):
        return self.problem

    def get_rationale(self):
        return self.rationale

    @staticmethod
    def load_from_string(problem_string):
        """
        s = "Problem: {self.problem}\nRationale:{self.rationale}"
        """
        problem = problem_string.split("Problem:")[1].split("Rationale:")[0].strip()
        rationale = problem_string.split("Rationale:")[1].strip()
        return Problem(problem, rationale)

    def load_problem_from_file(self, file_path):
        with open(file_path, "r") as file:
            problem_string = file.read()
            return self.load_from_string(problem_string)

    def save_problem_to_file(self, file_path):
        with open(file_path, "w") as file:
            file.write(str(self))

    def is_success(self):
        return self.success

    def set_success(self, success):
        self.success = success