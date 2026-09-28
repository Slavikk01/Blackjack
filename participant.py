from abc import ABC, abstractmethod

from hand import Hand


class Participant(ABC):
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

    @abstractmethod
    def choose_action(self):
        raise NotImplementedError
