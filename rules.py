class Rules:
    def __init__(self):
        self._blackjack_payout = 1.5
        self._dealer_stands_on = 17
        self._max_score = 21

    @property
    def blackjack_payout(self):
        return self._blackjack_payout

    @property
    def dealer_stands_on(self):
        return self._dealer_stands_on

    @property
    def max_score(self):
        return self._max_score

    def determine_winner(self, player, dealer):
        player_score = player.hand.score
        dealer_score = dealer.hand.score

        # Гравець перебрав
        if player.hand.is_bust:
            return "dealer"

        # Дилер перебрав
        if dealer.hand.is_bust:
            return "player"

        # У гравця Blackjack
        if player.hand.is_blackjack and not dealer.hand.is_blackjack:
            return "blackjack"

        # Blackjack у обох
        if player.hand.is_blackjack and dealer.hand.is_blackjack:
            return "push"

        # Порівняння результатів
        if player_score > dealer_score:
            return "player"

        if dealer_score > player_score:
            return "dealer"

        return "push"
