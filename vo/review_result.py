class ReviewResult:
    def __init__(self, review, feedback, rating, success=True):
        self.review = review
        self.feedback = feedback
        self.rating = rating
        self.success = success

    def __str__(self):
        return f"""Review:{self.review}\nFeedback:{self.feedback}\nRating (1-5):{self.rating}"""


    def get_review(self):
        return self.review

    def get_feedback(self):
        return self.feedback

    def get_rating(self):
        return self.rating

    @staticmethod
    def load_from_string(s):
        """
        s = Review:{self.review}\nFeedback:{self.feedback}\nRating (1-5):{self.rating}
        """
        try:
            review = s.split("Feedback:")[0].split("Review:")[1].strip()
            feedback = s.split("Rating (1-5):")[0].split("Feedback:")[1].strip()
            rating = s.split("Rating (1-5):")[1].strip()
            return ReviewResult(review, feedback, rating)
        except:
            print(s)
            import pdb;pdb.set_trace()


    @staticmethod
    def parse_method_review_rating(s, type="method", return_column_flag=False, set_random_default_value=False):
        """
        ["problem", 'method', 'experiment', 'ideate']
        """
        print(f"parse_method_review_rating: {s}")
        if type == "problem":
            metrics_key_words = ["Clarity:","Relevance:","Originality:","Feasibility:","Significance:"]
        elif type == "method":
            metrics_key_words = ["Clarity:","Validity:","Rigorousness:","Innovativeness:","Generalizability:"]
        elif type == "experiment":
            metrics_key_words = ["Clarity:", "Validity:", "Rigorousness:", "Feasibility:", "Reproducibility:"]
        else:
            raise NotImplemented
        score_result = dict()
        for line in str(s).split("\n"):
            line = line.replace("*", "")
            if line:
                for key_word in metrics_key_words:
                    if key_word in line:
                        score = line.split(key_word)[1].strip().replace(' ', '').replace('\n', '')
                        print(f"parse_method_review_rating | score: {score}")
                        if str(score).isdigit():
                            key = key_word.split(":")[0]
                            assert key not in score_result, f"key:{key}, scorev1:{score}, scorev2:{score_result[key]}"
                            score_result[key] = int(score)
                        else:
                            # Originality: 4. The problem is notably original, presenting a unique challenge or perspective that is well-differentiated from existing studies, contributing valuable new understanding to the field.
                            score = score.split('.')[0]
                            if str(score).isdigit():
                                key = key_word.split(":")[0]
                                assert key not in score_result, f"key:{key}, scorev1:{score}, scorev2:{score_result[key]}"
                                score_result[key] = int(score)
                            else:
                                score = score.split('-')[0]
                                if str(score).isdigit():
                                    key = key_word.split(":")[0]
                                    assert key not in score_result, f"key:{key}, scorev1:{score}, scorev2:{score_result[key]}"
                                    score_result[key] = int(score)
        metrics_key_words = [_.split(":")[0] for _ in metrics_key_words]
        print("score_result:", score_result)
        print("metrics_key_words:", metrics_key_words)
        if set_random_default_value:
            import random
            for key in metrics_key_words:
                if key not in score_result:
                    score_result[key] = random.randint(4, 5)
                    print("key:", key, "not in score_result, set random value:", score_result[key])
        if return_column_flag:
            return metrics_key_words, score_result
        return score_result

