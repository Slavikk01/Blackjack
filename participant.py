from hand import Hand


class Participant:
    def __init__(self):
        self._hand = Hand()

    @property
    def hand(self):
        return self._hand

    @property
    def score(self):
        return self._hand.score

    def reset_hand(self):
        self._hand.clear()
