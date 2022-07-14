import random
from poker import Card, Suit, Range

from TexasHoldem import TexasHoldem
from Player import Player
from Hand import Hand


deck = list(Card)
random.shuffle(deck)

flop = [deck.pop() for __ in range(3)]
turn = deck.pop()
river = deck.pop()

hand = [deck.pop() for __ in range(7)]
hand2 = [deck.pop() for __ in range(7)]

print(hand, Hand(hand), Hand(hand).tie_breakers)
print(hand2, Hand(hand2), Hand(hand2).tie_breakers)
print(Hand(hand), '<', Hand(hand2))
print(Hand(hand) < Hand(hand2))
print(Hand(hand), '==', Hand(hand2))
print(Hand(hand) == Hand(hand2))

# Range('XX').to_html()
# print(Range('XX').to_ascii())
# print(Range('AX 22+ K9+').to_ascii())

game = TexasHoldem()
game.addPlayer(Player('harrison', 100))
game.addPlayer(Player('austin', 100))
game.addPlayer(Player('paul', 100))
game.addPlayer(Player('daniel', 100))

# print(game)

game.startHand()

# print(deck[0], deck[1])
# print(deck[0].rank)
# print(deck[0].rank == deck[1].rank)
# print(deck[0].suit == Suit.CLUBS)


# print(hand)
# print(hand2)
# hand = pkr.Hand(hand)
# hand2 = pkr.Hand(hand2)
# print(hand)
# print(hand2)
