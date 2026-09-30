import unittest
from unittest.mock import patch

from card import Card
from dealer import Dealer
from player import Player


class TestPolymorphism(unittest.TestCase):
    def test_player_and_dealer_share_turn_decision_api(self):
        player = Player("Alice")
        dealer = Dealer()

        self.assertTrue(callable(getattr(player, "choose_action", None)))
        self.assertTrue(callable(getattr(dealer, "choose_action", None)))

    def test_dealer_uses_polymorphic_logic(self):
        dealer = Dealer()
        dealer.hand.add_card(Card("♠", "10"))
        dealer.hand.add_card(Card("♠", "6"))

        self.assertTrue(dealer.choose_action())

    def test_player_can_choose_to_stand(self):
        player = Player("Alice", money=1000)
        player.hand.add_card(Card("♠", "10"))
        player.hand.add_card(Card("♠", "8"))

        with patch("builtins.input", return_value="2"):
            self.assertEqual(player.choose_action(), "stand")


if __name__ == "__main__":
    unittest.main()
