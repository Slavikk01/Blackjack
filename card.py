class Card:
    def __init__(self, suit, rank):
        self._suit = suit
        self._rank = rank

    @property
    def suit(self):
        return self._suit

    @property
    def rank(self):
        return self._rank

    @property
    def value(self):
        # Туз спочатку має значення 11
        if self._rank == "A":
            return 11

        # Картинки мають значення 10
        if self._rank in ["J", "Q", "K"]:
            return 10

        return int(self._rank)

    def __str__(self):
        return f"{self._rank}{self._suit}"
