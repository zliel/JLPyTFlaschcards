from datetime import datetime

from PySide6.QtWidgets import QLabel, QWidget, QPushButton, QVBoxLayout, QHBoxLayout
from PySide6.QtCore import Qt, Slot, QObject, Signal

# noinspection PyUnresolvedReference
from __feature__ import snake_case, true_property

from models.Deck import Deck
import utils
from models.Flashcard import Flashcard
from theme import card_text_font, PaletteFactory, palettes


class CardWidgetSignals(QObject):
    card_passed = Signal(Flashcard)


class CardWidget(QWidget):
    """
    This widget displays a flashcard for the user to review. The user can click a button to reveal the answer, and then
    click one of two buttons to indicate whether they passed or failed the card. The card is then updated with the
    appropriate review date and the next card is displayed.
    """

    signals = CardWidgetSignals()

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
        settings = utils.load_config("settings.ini")
        palette = palettes[settings.get("USER", "theme", fallback="dark_blue")]

        pass_btn_style = f"background-color: {palette['background_300'].name()}; color: {palette['pass'].name()};"
        fail_btn_style = f"background-color: {palette['background_300'].name()}; color: {palette['fail'].name()};"

        # Question and Answer Labels
        self.question_label = QLabel("")
        self.question_label.font = card_text_font
        self.question_label.alignment = Qt.AlignCenter
        vbox.add_widget(self.question_label)

        self.answer_label = QLabel()
        self.answer_label.font = card_text_font
        self.answer_label.alignment = Qt.AlignCenter
        vbox.add_widget(self.answer_label)

        # Buttons (Show Answer, Fail, Pass)
        button_box = QHBoxLayout()

        self.show_answer_btn = QPushButton("Show Answer")
        self.show_answer_btn.clicked.connect(self.on_show_answer_click)
        # self.show_answer_btn.style_sheet = btn_style
        button_box.add_widget(self.show_answer_btn)

        self.fail_btn = QPushButton("Fail")
        self.fail_btn.clicked.connect(lambda: self.on_review_click(0))
        self.fail_btn.style_sheet = fail_btn_style
        self.fail_btn.hide()
        button_box.add_widget(self.fail_btn)

        self.pass_btn = QPushButton("Pass")
        self.pass_btn.clicked.connect(lambda: self.on_review_click(3))
        self.pass_btn.style_sheet = pass_btn_style
        self.pass_btn.hide()
        button_box.add_widget(self.pass_btn)

        vbox.add_layout(button_box)

        utils.setup_shortcuts(self, shortcuts={
            # Space will be to show answer or pass
            "Space": self.handle_space_bar,
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

        if grade >= 3:
            self.signals.card_passed.emit(self.cards[0])
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

    def handle_space_bar(self):
        """
        Handle the space bar press to show the answer or pass the card.
        :return: None
        """
        if self.answer_shown:
            self.on_review_click(3)
        else:
            self.on_show_answer_click()
