from uuid import uuid4

from models.Flashcard import Flashcard


class Deck:
    """
    A class to represent a deck of Flashcard objects.
    """

    def __init__(self, name, cards):
        """
        Constructor for the Deck class.
        :param name: The name of the deck, shown on the home page
        :param cards: A list of Flashcard objects in the deck
        """
        self.id = str(uuid4())
        self.name = name
        self.cards = cards
        self.is_modified = True
        # When a new deck is created, it is automatically modified, as it has not been saved yet

    def append_card(self, card: Flashcard) -> None:
        """
        Appends a Flashcard object to the deck.
        :param card: The Flashcard object to append
        :return: None
        """
        self.cards.append(card)
        self.is_modified = True

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

    def __hash__(self):
        return hash(self.id)
