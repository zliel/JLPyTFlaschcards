from PySide6.QtWidgets import QLabel, QWidget, QPushButton, QVBoxLayout, QHBoxLayout
from PySide6.QtCore import Qt, Slot

# noinspection PyUnresolvedReference
from __feature__ import snake_case, true_property

from models.Deck import Deck

class CardWidget(QWidget):
    def __init__(self, deck: Deck):
        super().__init__()
        self.deck = deck
        self.cards = self.deck.cards

        vbox = QVBoxLayout()

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

        self.set_layout(vbox)

        # Set up the first card
        self.update_card()


    @Slot()
    def on_show_answer_click(self):
        self.answer_label.text = ("<hr style=\"color: #fff; width: 50%;\">Back: " +
                                  self.cards[0].answer)
        self.answer_label.show()
        self.show_answer_btn.hide()
        self.pass_btn.show()
        self.fail_btn.show()


    @Slot()
    def on_review_click(self, score: int):
        self.cards[0].review(grade)
        self.update_card_list()

        self.show_answer_btn.show()
        self.pass_btn.hide()
        self.fail_btn.hide()
        self.update_card()

    def update_card_list(self):
        pass

    def update_card(self):
        pass
