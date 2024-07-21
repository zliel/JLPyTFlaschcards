from PySide6.QtWidgets import QLabel, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLineEdit, QTextEdit
from PySide6.QtCore import Qt, Slot, Signal, QObject

# noinspection PyUnresolvedReference
from __feature__ import snake_case, true_property

from models.Flashcard import Flashcard


class CardEditSignals(QObject):
    card_edited = Signal(Flashcard, Flashcard)


class CardEditWidget(QWidget):

    signals = CardEditSignals()
    def __init__(self, card: Flashcard = None) -> None:
        super().__init__()
        self.layout = QVBoxLayout()
        self.card = card

        self.front_label = QLabel("Front:")
        self.layout.add_widget(self.front_label)
        self.front_input = QTextEdit()
        self.layout.add_widget(self.front_input)

        self.back_label = QLabel("Back:")
        self.layout.add_widget(self.back_label)
        self.back_input = QTextEdit()
        self.layout.add_widget(self.back_input)

        self.tags_label = QLabel("Tags (seperate by spaces):")
        self.layout.add_widget(self.tags_label)
        self.tags_input = QLineEdit()
        self.layout.add_widget(self.tags_input)

        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.save_card)
        self.layout.add_widget(self.save_button)

        self.set_layout(self.layout)

        if self.card:
            self.load_card()
        # self.show()

    def load_card(self):
        self.front_input.set_text(self.card.question)
        self.back_input.set_text(self.card.answer)
        # example: "tag1 tag2 tag3"
        self.tags_input.text = " ".join(self.card.tags)

    @Slot()
    def save_card(self):
        old_card = Flashcard(question=self.card.question, answer=self.card.answer, tags=self.card.tags)
        self.card.question = self.front_input.plain_text
        self.card.answer = self.back_input.plain_text
        self.card.tags = self.tags_input.text.split()

        self.signals.card_edited.emit(self.card, old_card)
        self.close()
