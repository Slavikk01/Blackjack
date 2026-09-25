class Hand:
    def __init__(self):
        self._cards = []

    @property
    def cards(self):
        return self._cards

    @property
    def score(self):
        total = 0
        aces = 0

        # FOR EACH — рахуємо всі карти
        for card in self._cards:
            total += card.value

            if card.rank == "A":
                aces += 1

        # Якщо перебрали 21, туз перетворюється з 11 на 1
        while total > 21 and aces > 0:
            total -= 10
            aces -= 1

        return total

    @property
    def is_blackjack(self):
        return len(self._cards) == 2 and self.score == 21

    @property
    def is_bust(self):
        return self.score > 21

    def add_card(self, card):
        self._cards.append(card)

    def clear(self):
        self._cards.clear()

    def show_cards(self, hide_first=False):
        result = []

        for index, card in enumerate(self._cards):
            if hide_first and index == 0:
                result.append("??")
            else:
                result.append(str(card))

        return " ".join(result)
