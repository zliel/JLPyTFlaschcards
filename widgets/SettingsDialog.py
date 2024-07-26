from configparser import ConfigParser

from PySide6.QtGui import QIntValidator
from PySide6.QtWidgets import QLabel, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLineEdit, QDialog
from PySide6.QtCore import Qt, Slot

# noinspection PyUnresolvedReference
from __feature__ import snake_case, true_property

from theme import default_text_font



class SettingsDialog(QDialog):
    def __init__(self, settings: ConfigParser):
        super().__init__()
        self.window_title = "Settings"
        self.settings = settings
        self.layout = QVBoxLayout()
        self.layout.alignment = Qt.AlignCenter

        review_layout = QHBoxLayout()
        self.review_limit_label = QLabel("Review Limit:")
        self.review_limit_label.font = default_text_font
        review_layout.add_widget(self.review_limit_label)
        self.review_limit_input = QLineEdit()
        self.review_limit_input.font = default_text_font
        only_int_validator = QIntValidator()
        only_int_validator.set_range(0, 1000)
        self.review_limit_input.validator = only_int_validator
        review_layout.add_widget(self.review_limit_input)
        self.layout.add_layout(review_layout)

        new_cards_layout = QHBoxLayout()
        self.new_cards_limit_label = QLabel("New Cards Limit:")
        self.new_cards_limit_label.font = default_text_font
        new_cards_layout.add_widget(self.new_cards_limit_label)
        self.new_cards_limit_input = QLineEdit()
        self.new_cards_limit_input.font = default_text_font
        self.new_cards_limit_input.validator = only_int_validator
        new_cards_layout.add_widget(self.new_cards_limit_input)
        self.layout.add_layout(new_cards_layout)

        self.save_button = QPushButton("Save")
        self.layout.add_widget(self.save_button)

        self.resize(300, 200)
        self.set_layout(self.layout)