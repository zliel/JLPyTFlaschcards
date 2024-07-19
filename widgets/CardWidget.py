from datetime import datetime

from PySide6.QtWidgets import QLabel, QWidget, QPushButton, QVBoxLayout, QHBoxLayout
from PySide6.QtCore import Qt, Slot
from PySide6.QtGui import QKeySequence, QShortcut

# noinspection PyUnresolvedReference
from __feature__ import snake_case, true_property

from models.Deck import Deck
import utils


class CardWidget(QWidget):
    """
    This widget displays a flashcard for the user to review. The user can click a button to reveal the answer, and then
    click one of two buttons to indicate whether they passed or failed the card. The card is then updated with the
    appropriate review date and the next card is displayed.
    """

    def __init__(self, deck: Deck):
        """
        Initialize the CardWidget with a deck of flashcards.
        :param deck: The deck of flashcards to review
        """
        super().__init__()
        self.deck = deck
        self.cards = self.deck.cards
        self.answer_shown = False

        # Ensure that the only cards in the list are those that need to be reviewed, and sort them by review date
        self.update_card_list()

        vbox = QVBoxLayout()
        btn_style = "background-color: #5a6363; color: #fff;"

        # Question and Answer Labels
        self.question_label = QLabel("")
        self.question_label.alignment = Qt.AlignCenter
        vbox.add_widget(self.question_label)

        self.answer_label = QLabel()
        self.answer_label.alignment = Qt.AlignCenter
        vbox.add_widget(self.answer_label)

        # Buttons (Show Answer, Fail, Pass)
        button_box = QHBoxLayout()

        self.show_answer_btn = QPushButton("Show Answer")
        self.show_answer_btn.clicked.connect(self.on_show_answer_click)
        self.show_answer_btn.style_sheet = btn_style
        button_box.add_widget(self.show_answer_btn)

        self.fail_btn = QPushButton("Fail")
        self.fail_btn.clicked.connect(lambda: self.on_review_click(0))
        self.fail_btn.style_sheet = btn_style
        self.fail_btn.hide()
        button_box.add_widget(self.fail_btn)

        self.pass_btn = QPushButton("Pass")
        self.pass_btn.clicked.connect(lambda: self.on_review_click(3))
        self.pass_btn.style_sheet = btn_style
        self.pass_btn.hide()
        button_box.add_widget(self.pass_btn)

        vbox.add_layout(button_box)

        utils.setup_shortcuts(self, shortcuts={
            # Space will be to show answer or pass
            "Space": self.on_show_answer_click if not self.answer_shown else self.on_review_click(3),
            "1": lambda: self.on_review_click(0) if self.answer_shown else None,
            "2": lambda: self.on_review_click(3) if self.answer_shown else None
        })
        self.set_layout(vbox)

        # Set up the first card
        self.update_card()

    @Slot()
    def on_show_answer_click(self):
        """
        Show the answer to the current flashcard.
        :return: None
        """
        if len(self.cards) == 0:
            return
        self.answer_label.text = ("<hr style=\"color: #fff; width: 50%;\">Back: " +
                                  self.cards[0].answer)
        self.answer_label.show()
        self.show_answer_btn.hide()
        self.pass_btn.show()
        self.fail_btn.show()
        self.answer_shown = True

    @Slot()
    def on_review_click(self, grade: int):
        """
        Review the current flashcard with the given grade.
        :param grade: The grade of the review (0-5)
        :return: None
        """
        if not self.answer_shown or len(self.cards) == 0:
            return
        self.cards[0].review(grade)
        # When a card is reviewed, the deck is modified, for the save function to know to save this particular deck
        self.deck.is_modified = True
        self.update_card_list()

        self.show_answer_btn.show()
        self.pass_btn.hide()
        self.fail_btn.hide()
        self.update_card()
        self.answer_shown = False

    def update_card_list(self):
        """
        Update the list of cards to only include those that are due for review.
        :return:  None
        """
        self.cards = [card for card in self.cards if card.next_review_date <= datetime.now()]
        # Sort the cards by next review
        self.cards = sorted(self.cards, key=lambda card: card.next_review_date)

    def update_card(self):
        """
        Update the current card being displayed.
        :return: None
        """
        # If there are no cards left, display a message
        if len(self.cards) == 0:
            self.question_label.text = "No more cards to review"
            self.answer_label.hide()
            self.show_answer_btn.hide()
            self.pass_btn.hide()
            self.fail_btn.hide()
        else:
            # Otherwise, display the front of the card
            card = self.cards[0]
            self.question_label.text = "Front: " + card.question
            self.answer_label.text = ""
