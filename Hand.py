from poker import Suit, Rank

points = {
  Rank('2'): 2,
  Rank('3'): 3,
  Rank('4'): 4,
  Rank('5'): 5,
  Rank('6'): 6,
  Rank('7'): 7,
  Rank('8'): 8,
  Rank('9'): 9,
  Rank('T'): 10,
  Rank('J'): 11,
  Rank('Q'): 12,
  Rank('K'): 13,
  Rank('A'): 14
} 
suitSort = {
  Suit.CLUBS: 0,
  Suit.DIAMONDS: 1,
  Suit.HEARTS: 2,
  Suit.SPADES: 3
}
handRanks = {
  'high card': 0,
  'pair': 1,
  'two pair': 2,
  'set': 3,
  'straight': 4,
  'flush': 5,
  'full house': 6,
  'quads': 7,
  'straight flush': 8
}

class Hand(object):

  def __init__(self, cards=[]):
    self.cards = cards        # list of cards in the hand
    self.hand = 'high card'   # ranking of the given hand
    self.tie_breakers = []    # list of values to rank hands given they have the same ranking
    self.score()              # scores the hand

  # gets what the hand is worth
  def score(self):
    suits = [[], [], [], []]  # list of lists of cards with the same suit
    combos = []               # list of lists of cards with the same rank
    straights = []            # list of lists of touching cards

    hand = sorted(self.cards)

    last_value = 0

    for card in hand:
      if points[card.rank] == last_value:
        combos[-1].append(card)
      elif points[card.rank] == last_value+1:
        straights[-1].append(card)
        combos.append([card])
      else:
        straights.append([card])
        combos.append([card])

      suits[suitSort[card.suit]].append(card)
      
      last_value = points[card.rank]

    isFlush = False
    for suit in suits:
      if len(suit) >= 5:
        isFlush = True

    isStraight = False
    for straight in straights:
      if len(straight) >= 5:
        isStraight = True

    pairs = 0
    sets = 0
    quads = 0

    for combo in combos:
      if len(combo) == 2:
        pairs += 1
        combo = combo[0].rank
      elif len(combo) == 3:
        sets += 1
        combo = combo[0].rank
      elif len(combo) == 4:
        quads += 1
        combo = combo[0].rank

    if quads >= 1:
      self.hand = 'quads'
      self.tie_breakers.append(points[combos[-1][0]])
      if len(combos[-1]) == 4:
        self.tie_breakers.append(points[combos[-2][0]])
      else: 
        for combo in reversed(combos):
          if len(combo) == 4:
            self.tie_breakers.insert(0, points[combo[0].rank])
            return

    elif sets >= 2 or (sets >= 1 and pairs >= 1):
      self.hand = 'full house'
      set_found = False
      for combo in reversed(combos):
        if not set_found and len(combo) == 3:
          self.tie_breakers.insert(0, points[combo[0].rank])
          set_found = True
        elif len(combo) >= 2:
          self.tie_breakers.append(points[combo[0].rank])

        if len(self.tie_breakers) == 2:
          return

    elif isFlush:
      self.hand = 'flush'
      for suit in suits:
        if len(suit) >= 5:
          for i in range(-1, -6, -1):
            self.tie_breakers.append(points[suit[i].rank])
          return

    elif isStraight:
      self.hand = 'straight'
      for straight in reversed(straights):
        if len(straight) >= 5:
          self.tie_breakers = [points[straight[-1].rank]]

    elif sets == 1:
      self.hand = 'set'
      singles = 0
      for combo in reversed(combos):
        if len(combo) == 3:
          self.tie_breakers.insert(0, points[combo[0].rank])
        elif singles < 2:
          self.tie_breakers.append(points[combo[0].rank])
          singles += 1

        if len(self.tie_breakers) == 3:
          return

    elif pairs >= 2:
      self.hand = 'two pair'
      singles = 0
      duos = 0
      for combo in reversed(combos):
        if duos < 2 and len(combo) == 2:
          self.tie_breakers.insert(0, points[combo[0].rank])
          duos += 1
        elif singles < 1:
          self.tie_breakers.append(points[combo[0].rank])
          singles += 1

        if len(self.tie_breakers) == 3:
          self.tie_breakers[1], self.tie_breakers[0] = self.tie_breakers[0], self.tie_breakers[1]
          return

    elif pairs == 1:
      self.hand = 'pair'
      singles = 0
      for combo in reversed(combos):
        if len(combo) == 2:
          self.tie_breakers.insert(0, points[combo[0].rank])
        elif singles < 3:
          self.tie_breakers.append(points[combo[0].rank])
          singles += 1

        if len(self.tie_breakers) == 4:
          return

    else:
      self.hand = 'high card'
      for i in range(-1, -6, -1):
        self.tie_breakers.append(points[hand[i].rank])

  def __lt__ (self, other):
    if handRanks[self.hand] == handRanks[other.hand]:
      for i in range(len(self.tie_breakers)):
        if self.tie_breakers[i] != other.tie_breakers[i]:
          return self.tie_breakers[i] < other.tie_breakers[i]

    return handRanks[self.hand] < handRanks[other.hand]

  def __gt__ (self, other):
    return other.__lt__(self)

  def __eq__ (self, other):
    if handRanks[self.hand] == handRanks[other.hand]:
      for i in range(len(self.tie_breakers)):
        if self.tie_breakers[i] != other.tie_breakers[i]:
          return False
      return True
    return False

  def __ne__ (self, other):
    return not self.__eq__(other)

  def __repr__(self):
    return self.hand