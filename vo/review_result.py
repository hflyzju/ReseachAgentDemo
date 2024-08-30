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
