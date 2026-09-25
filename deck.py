import random

from card import Card


class Deck:
    def __init__(self):
        self._cards = []
        self.create_deck()
        self.shuffle()

    @property
    def cards(self):
        return self._cards

    @property
    def count(self):
        return len(self._cards)

    def create_deck(self):
        suits = ["♥", "♦", "♣", "♠"]
        ranks = [
            "2", "3", "4", "5", "6", "7", "8", "9", "10",
            "J", "Q", "K", "A"
        ]

        # FOR EACH — перебираємо кожну масть
        for suit in suits:
            # FOR EACH — перебираємо кожне значення карти
            for rank in ranks:
                self._cards.append(Card(suit, rank))

    def shuffle(self):
        random.shuffle(self._cards)

    def draw_card(self):
        if len(self._cards) == 0:
            self.create_deck()
            self.shuffle()

        return self._cards.pop()
