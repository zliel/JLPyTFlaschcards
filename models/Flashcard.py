from datetime import datetime, timedelta
from uuid import uuid4


class Flashcard:
    def __init__(self, question, answer):
        self.id = str(uuid4())
        self.question = question
        self.answer = answer
        self.next_review_date = datetime.now()
        self.repetitions = 0
        self.easiness_factor = 2.5
        self.interval = 0

    def review(self, quality: int) -> None:
        # Simplified SM-2 Algorithm for spaced repetition
        # In our case, this is if the user clicks "Pass"
        if quality >= 3:
            if self.repetitions == 0:
                self.interval = 1
            elif self.repetitions == 1:
                self.interval = 6
            else:
                self.interval = round(self.repetitions * self.easiness_factor)
            self.repetitions += 1
        else:
            # If the user clicks "Fail", reset the card's repetitions and interval
            self.repetitions = 0
            self.interval = 0  # Slight adjustment to the algorithm to make the user review the card again on the same day

        # Update the easiness factor
        self.easiness_factor = self.easiness_factor + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02))
        if self.easiness_factor < 1.3:
            self.easiness_factor = 1.3

        # Update the next review date
        self.next_review_date = datetime.now() + timedelta(days=self.interval)

    def print_stats(self) -> None:
        print(f"ID: {self.id}")
        print(f"Question: {self.question}")
        print(f"Answer: {self.answer}")
        print(f"Next Review Date: {self.next_review_date}")
        print(f"Repetitions: {self.repetitions}")
        print(f"Easiness Factor: {self.easiness_factor}")
        print(f"Interval: {self.interval}")

    def get_stats(self) -> dict:
        return {
            "id": self.id,
            "question": self.question,
            "answer": self.answer,
            "next_review_date": self.next_review_date,
            "repetitions": self.repetitions,
            "easiness_factor": self.easiness_factor,
            "interval": self.interval
        }

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
