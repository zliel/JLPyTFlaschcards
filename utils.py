import os
import csv
from typing import List

from models.Deck import Deck


def save_deck_to_csv(deck: Deck, directory: str) -> None:
    if not deck.is_modified:
        print(f"Deck {deck.name} has not been modified")
        return  # Skip saving if the deck hasn't been modified

    if not os.path.exists(directory):
        os.makedirs(directory)

    filename = f"{directory}/{deck.name}.csv"
    print(f"Saving deck to {filename}")
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Deck ID', 'Deck Name', 'Card ID', 'Question', 'Answer', 'Next Review Date', 'Repetitions',
                         'Easiness Factor', 'Interval'])
        for card in deck.cards:
            writer.writerow(
                [deck.id, deck.name, card.id, card.question, card.answer, card.next_review_date, card.repetitions,
                 card.easiness_factor, card.interval])
    deck.is_modified = False  # Reset the modified flag after saving


def save_decks_to_csv(decks: List[Deck], directory: str) -> None:
    for deck in decks:
        save_deck_to_csv(deck, directory)
