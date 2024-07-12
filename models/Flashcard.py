from datetime import datetime, timedelta


class Flashcard:
    def __init__(self, question, answer):
        self.question = question
        self.answer = answer
        self.next_review_date = datetime.now()