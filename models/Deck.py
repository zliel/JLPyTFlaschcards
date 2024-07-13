from uuid import uuid4


class Deck:
    def __init__(self, name, cards):
        self.id = str(uuid4())
        self.name = name
        self.cards = cards

    def __str__(self):
        return f"Deck: {self.name}\nID: {self.id}\nCards: {self.cards}"

    def __eq__(self, other):
        return self.name == other.name and self.cards == other.cards

    def __ne__(self, other):
        return not self == other

    def __lt__(self, other):
        return self.name < other.name

    def __le__(self, other):
        return self.name <= other.name

    def __gt__(self, other):
        return not self <= other

    def __ge__(self, other):
        return not self < other

    def __repr__(self):
        return f"Deck({self.id}, {self.name}, {self.cards})"