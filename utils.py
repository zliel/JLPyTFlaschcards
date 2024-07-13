import os
import csv
from typing import List

from models.Deck import Deck
from models.Flashcard import Flashcard


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


def load_deck_from_csv(filename: str) -> Deck:
    with open(filename, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        cards = []
        deck_name = ""
        for row in reader:
            if not deck_name:  # Get the deck name from the first row
                deck_name = row['Deck Name']
            card = Flashcard(
                question=row['Question'],
                answer=row['Answer'],
                next_review_date=row['Next Review Date'],
                repetitions=int(row['Repetitions']),
                easiness_factor=float(row['Easiness Factor']),
                interval=int(row['Interval']),
                id=row['Card ID']
            )
            cards.append(card)
        deck = Deck(name=deck_name, cards=cards)
        return deck


def load_decks_from_csv(directory: str) -> List[Deck]:
    decks = []
    for filename in os.listdir(directory):
        if filename.endswith(".csv"):
            deck = load_deck_from_csv(f"{directory}/{filename}")
            decks.append(deck)
    return decks
