from uuid import uuid4
from datetime import datetime
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
        self.session_review_cards = 0
        self.session_new_cards = 0

    def append_card(self, card: Flashcard) -> None:
        """
        Appends a Flashcard object to the deck.
        :param card: The Flashcard object to append
        :return: None
        """
        self.cards.append(card)
        self.is_modified = True

    def get_filtered_cards(self, max_reviews: int, max_new: int) -> (list, int):
        """
        Get a filtered list of cards based on the number of reviews and new cards.
        :param max_reviews: Maximum number of review cards
        :param max_new: Maximum number of new cards
        :return: List of filtered cards, and the total number of cards that will be reviewed
        """
        today = datetime.now().date()
        review_cards = [card for card in self.cards if card.next_review_date.date() <= today and card.repetitions > 0]
        new_cards = [card for card in self.cards if card.next_review_date.date() >= today and card.repetitions == 0]
        today = datetime.now()
        review_cards = [card for card in self.cards if card.next_review_date <= today and card.repetitions > 0]
        new_cards = [card for card in self.cards if card.next_review_date <= today and card.repetitions == 0]

        review_cards = review_cards[:max_reviews - self.session_review_cards]
        new_cards = new_cards[:max_new - self.session_new_cards]
        num_of_cards = len(review_cards) + len(new_cards)

        return review_cards + new_cards, num_of_cards

    def handle_card_review(self, is_new_card: bool):
        """
        Handle the review of a card.
        :param is_new_card: True if the card is new, False otherwise
        :return: None
        """
        if is_new_card:
            self.session_new_cards += 1
        else:
            self.session_review_cards += 1

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
