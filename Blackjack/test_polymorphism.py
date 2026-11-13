import unittest
from unittest.mock import patch

from card import Card
from dealer import Dealer
from game import BlackjackGame
from game_interface import GameInterface
from player import Player
from rock_paper_scissors import RockPaperScissorsGame


class TestPolymorphism(unittest.TestCase):
    def test_player_and_dealer_share_turn_decision_api(self):
        player = Player("Alice")
        dealer = Dealer()

        self.assertTrue(callable(getattr(player, "choose_action", None)))
        self.assertTrue(callable(getattr(dealer, "choose_action", None)))

    def test_blackjack_implements_reusable_game_interface(self):
        game = BlackjackGame("Alice")

        self.assertIsInstance(game, GameInterface)
        self.assertEqual(game.players, game.participants)
        self.assertIn(game.player, game.players)

    def test_game_interface_does_not_require_inheritance(self):
        class OtherGame:
            @property
            def players(self):
                return ["Alice"]

            def make_move(self, player):
                return f"{player} moved"

        game = OtherGame()

        self.assertIsInstance(game, GameInterface)
        self.assertEqual(game.make_move(game.players[0]), "Alice moved")

    def test_make_move_applies_the_chosen_action(self):
        game = BlackjackGame("Alice")
        player = game.player
        player.hand.add_card(Card("♠", "10"))

        with patch.object(player, "choose_action", return_value="hit"):
            with patch.object(
                game.deck,
                "draw_card",
                return_value=Card("♥", "5")
            ):
                self.assertEqual(game.make_move(player), "hit")

        self.assertEqual(player.hand.score, 15)

    def test_rock_paper_scissors_implements_game_interface(self):
        game = RockPaperScissorsGame("Alice")

        self.assertIsInstance(game, GameInterface)
        self.assertEqual(game.players, ["Alice", "Комп'ютер"])

    def test_rock_paper_scissors_tracks_round_winner(self):
        game = RockPaperScissorsGame("Alice")

        with patch("builtins.input", side_effect=["1"]):
            with patch(
                "rock_paper_scissors.random.choice",
                return_value="ножиці"
            ):
                game.play_round()

        self.assertEqual(game.scores["Alice"], 1)
        self.assertEqual(game.scores["Комп'ютер"], 0)

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
