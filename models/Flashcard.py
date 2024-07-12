from datetime import datetime, timedelta


class Flashcard:
    def __init__(self, question, answer):
        self.question = question
        self.answer = answer
        self.next_review_date = datetime.now()

    def __str__(self):
        return f"Question: {self.question}\nAnswer: {self.answer}\nNext Review Date: {self.next_review_date}"

    def __eq__(self, other):
        return self.question == other.question and self.answer == other.answer

    def __ne__(self, other):
        return not self == other

    def __lt__(self, other):
        return self.next_review_date < other.next_review_date

    def __le__(self, other):
        return self.next_review_date <= other.next_review_date

    def __gt__(self, other):
        return self.next_review_date > other.next_review_date

    def __ge__(self, other):
        return self.next_review_date >= other.next_review_date

    def __repr__(self):
        return f"Flashcard({self.question}, {self.answer}, {self.next_review_date})"
