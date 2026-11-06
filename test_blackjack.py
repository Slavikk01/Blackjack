import io
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch

from card import Card
from dealer import Dealer
from deck import Deck
from game import BlackjackGame
from hand import Hand
from player import Player
from rules import Rules


class TestCardAndDeck(unittest.TestCase):
    def test_card_values_and_string_representation(self):
        self.assertEqual(Card("♠", "A").value, 11)
        self.assertEqual(Card("♥", "Q").value, 10)
        self.assertEqual(Card("♦", "7").value, 7)
        self.assertEqual(str(Card("♣", "10")), "10♣")

    def test_new_deck_contains_each_card_once(self):
        deck = Deck()

        self.assertEqual(deck.count, 52)
        self.assertEqual(
            {(card.suit, card.rank) for card in deck.cards},
            {
                (suit, rank)
                for suit in ("♥", "♦", "♣", "♠")
                for rank in (
                    "2", "3", "4", "5", "6", "7", "8", "9", "10",
                    "J", "Q", "K", "A",
                )
            },
        )

    def test_empty_deck_recreates_it_before_drawing(self):
        deck = Deck()
        deck.cards.clear()

        with patch.object(deck, "shuffle") as shuffle:
            card = deck.draw_card()

        self.assertIsInstance(card, Card)
        self.assertEqual(deck.count, 51)
        shuffle.assert_called_once_with()


class TestHand(unittest.TestCase):
    def test_score_counts_ace_as_one_when_needed(self):
        hand = Hand()
        for rank in ("A", "A", "9"):
            hand.add_card(Card("♠", rank))

        self.assertEqual(hand.score, 21)
        self.assertFalse(hand.is_bust)

    def test_blackjack_requires_exactly_two_cards(self):
        hand = Hand()
        hand.add_card(Card("♠", "A"))
        hand.add_card(Card("♥", "K"))
        self.assertTrue(hand.is_blackjack)

        hand.add_card(Card("♦", "2"))
        self.assertFalse(hand.is_blackjack)

    def test_bust_and_hidden_card_display(self):
        hand = Hand()
        hand.add_card(Card("♠", "10"))
        hand.add_card(Card("♥", "8"))
        hand.add_card(Card("♦", "5"))

        self.assertTrue(hand.is_bust)
        self.assertEqual(hand.show_cards(), "10♠ 8♥ 5♦")
        self.assertEqual(hand.show_cards(hide_first=True), "?? 8♥ 5♦")

    def test_clear_removes_all_cards(self):
        hand = Hand()
        hand.add_card(Card("♠", "6"))

        hand.clear()

        self.assertEqual(hand.cards, [])
        self.assertEqual(hand.score, 0)


class TestRules(unittest.TestCase):
    def setUp(self):
        self.rules = Rules()
        self.player = Player("Alice")
        self.dealer = Dealer()

    def give_cards(self, participant, *ranks):
        for rank in ranks:
            participant.hand.add_card(Card("♠", rank))

    def test_blackjack_payout_and_limits(self):
        self.assertEqual(self.rules.blackjack_payout, 1.5)
        self.assertEqual(self.rules.dealer_stands_on, 17)
        self.assertEqual(self.rules.max_score, 21)

    def test_player_bust_loses_even_if_dealer_also_busts(self):
        self.give_cards(self.player, "10", "9", "5")
        self.give_cards(self.dealer, "10", "9", "5")

        self.assertEqual(
            self.rules.determine_winner(self.player, self.dealer), "dealer"
        )

    def test_dealer_bust_means_player_wins(self):
        self.give_cards(self.player, "10", "8")
        self.give_cards(self.dealer, "10", "9", "5")

        self.assertEqual(
            self.rules.determine_winner(self.player, self.dealer), "player"
        )

    def test_blackjack_and_equal_scores(self):
        self.give_cards(self.player, "A", "K")
        self.give_cards(self.dealer, "10", "8")
        self.assertEqual(
            self.rules.determine_winner(self.player, self.dealer), "blackjack"
        )

        self.dealer.reset_hand()
        self.give_cards(self.dealer, "A", "Q")
        self.assertEqual(
            self.rules.determine_winner(self.player, self.dealer), "push"
        )

    def test_higher_score_wins_and_equal_score_pushes(self):
        self.give_cards(self.player, "10", "9")
        self.give_cards(self.dealer, "10", "8")
        self.assertEqual(
            self.rules.determine_winner(self.player, self.dealer), "player"
        )

        self.dealer.reset_hand()
        self.give_cards(self.dealer, "10", "9")
        self.assertEqual(
            self.rules.determine_winner(self.player, self.dealer), "push"
        )


class TestPlayerAndDealer(unittest.TestCase):
    def test_bet_validation_and_money_settlement(self):
        player = Player("Alice", money=100)
        output = io.StringIO()

        with redirect_stdout(output):
            self.assertFalse(player.place_bet(0))
            self.assertFalse(player.place_bet(101))

        self.assertTrue(player.place_bet(40))
        self.assertEqual(player.money, 60)
        player.win()
        self.assertEqual(player.money, 140)
        self.assertEqual(player.bet, 0)

        self.assertTrue(player.place_bet(20))
        player.win(1.5)
        self.assertEqual(player.money, 150)

    def test_loss_and_push_settle_bet(self):
        player = Player("Alice", money=100)

        player.place_bet(25)
        player.push()
        self.assertEqual(player.money, 100)
        self.assertEqual(player.bet, 0)

        player.place_bet(25)
        player.lose()
        self.assertEqual(player.money, 75)
        self.assertEqual(player.bet, 0)

    def test_dealer_hits_below_17_and_stands_at_17(self):
        dealer = Dealer()
        dealer.hand.add_card(Card("♠", "10"))
        dealer.hand.add_card(Card("♥", "6"))
        self.assertEqual(dealer.choose_action(), "hit")

        dealer.hand.add_card(Card("♦", "A"))
        self.assertEqual(dealer.score, 17)
        self.assertEqual(dealer.choose_action(), "stand")


class TestBlackjackGame(unittest.TestCase):
    def setUp(self):
        self.game = BlackjackGame("Alice")

    def test_initial_deal_gives_two_cards_to_each_participant(self):
        self.game.deck.cards[:] = [
            Card("♣", "7"),
            Card("♣", "9"),
            Card("♥", "8"),
            Card("♠", "10"),
        ]

        with redirect_stdout(io.StringIO()):
            self.game.deal_initial_cards()

        self.assertEqual(self.game.player.hand.show_cards(), "10♠ 8♥")
        self.assertEqual(self.game.dealer.hand.show_cards(), "9♣ 7♣")

    def test_start_round_player_blackjack_pays_blackjack_multiplier(self):
        self.game.deck.cards[:] = [
            Card("♣", "7"),
            Card("♣", "9"),
            Card("♥", "K"),
            Card("♠", "A"),
        ]

        with patch("builtins.input", return_value="100"):
            with redirect_stdout(io.StringIO()):
                self.game.start_round()

        self.assertEqual(self.game.round_number, 1)
        self.assertEqual(self.game.player.money, 1050)
        self.assertEqual(self.game.player.bet, 0)

    def test_start_round_stand_then_dealer_win(self):
        self.game.deck.cards[:] = [
            Card("♥", "5"),
            Card("♣", "7"),
            Card("♣", "9"),
            Card("♥", "8"),
            Card("♠", "10"),
        ]

        with patch("builtins.input", side_effect=["100", "2"]):
            with redirect_stdout(io.StringIO()):
                self.game.start_round()

        self.assertEqual(self.game.player.money, 900)
        self.assertEqual(self.game.player.bet, 0)
        self.assertEqual(self.game.dealer.hand.score, 21)

    def test_run_marks_game_over_when_player_has_no_money(self):
        self.game.player._money = 0

        with redirect_stdout(io.StringIO()):
            self.game.run()

        self.assertTrue(self.game.game_over)


if __name__ == "__main__":
    unittest.main()
