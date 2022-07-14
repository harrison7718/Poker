class Player(object):
  def __init__(self, name=None, chips=0):
    self.name = name
    self.chips = chips
    self.bet = 0
    self.stake = 0
    self.cards = []
    self.active = True
    self.win = False

  def printCards(self):
    print(self.cards)

  def __repr__(self):
    repr = self.name + ': ' + str(self.chips) + ' chips' 
    return repr