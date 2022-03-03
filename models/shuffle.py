from .card.card import Card
from .position import Position
from .positions import Positions
import sys


class Shuffle:
    def __init__(self, deck, type):
        self.type = type
        self.deck = deck
        self.amount = 1
        self.tracked_cards = []
        self.times_shuffled = 0
        self.shuffle_until = None

    def times(self, amount):
        self.amount = amount
        return self

    def tracking_card(self, idx):
        if idx < 1 or idx > len(self.deck):
            return print("invalid position")

        if len(self.tracked_cards) >= 2:
            return print("can only track 2 positions exclusively")

        self.tracked_cards.append(self.deck[idx - 1])
        return self

    def tracking_cards(self, idx1, idx2):
        if idx1 < 1 or idx2 < 1 or idx1 > len(self.deck) or idx2 > len(self.deck):
            return print("invalid position")

        if len(self.tracked_cards) >= 2:
            return print("can only track 2 positions exclusively")

        self.tracked_cards = [self.deck[idx1 - 1], self.deck[idx2 - 1]]

        return self

    def until(self, condition):
        if condition == "TOUCHING":
            self.shuffle_until = "TOUCHING"

            return self

        elif condition == "CARD_IS_LAST":
            self.shuffle_until = "CARD_IS_LAST"

            return self

    def in_shuffle(self):
        first_tracked_card = self.tracked_cards[0]
        first_tracked_card_pos = Position(first_tracked_card, 0)

        second_tracked_card = self.tracked_cards[-1]
        second_tracked_card_pos = Position(second_tracked_card, 0)

        self.amount = sys.maxsize if self.shuffle_until else self.amount

        while self.times_shuffled < self.amount:
            shuffled_cards = []

            mid_idx = (len(self.deck)) // 2

            top_half = self.deck[:mid_idx]
            bottom_half = self.deck[mid_idx:]

            for i in range(len(top_half)):
                shuffled_cards.append(bottom_half[i])
                shuffled_cards.append(top_half[i])

                first_tracked_card_pos.update(
                    bottom_half[i],
                    top_half[i],
                    len(shuffled_cards),
                )

                second_tracked_card_pos.update(
                    bottom_half[i],
                    top_half[i],
                    len(shuffled_cards),
                )

            positions = Positions(
                first_tracked_card_pos.value,
                second_tracked_card_pos.value,
                len(self.deck),
            )

            if (
                positions.is_now_last("first") and self.shuffle_until == "CARD_IS_LAST"
            ) or (positions.is_touching() and self.shuffle_until == "TOUCHING"):
                return self

            self.deck = shuffled_cards
            self.times_shuffled += 1

        return positions

    def execute(self):
        if self.type == "in":
            return self.in_shuffle()