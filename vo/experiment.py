class Experiment:
    def __init__(self, experimentDesign, experimentDesignRationale, success=True):
        self.experimentDesign = experimentDesign
        self.experimentDesignRationale = experimentDesignRationale
        self.success = success

    def __str__(self):
        return f"""Experiment:{self.experimentDesign}\nRationale:{self.experimentDesignRationale}"""

    def get_result(self):
        return self.experimentDesign

    def get_rationale(self):
        return self.experimentDesignRationale

    @staticmethod
    def load_from_string(experiment_string):
        """
        s = "Method: {self.problem}\nRationale:{self.rationale}"
        """
        experimentDesign = experiment_string.split("Experiment:")[1].split("Rationale:")[0].strip()
        rationale = experiment_string.split("Rationale:")[1].strip()
        return Experiment(experimentDesign, rationale)