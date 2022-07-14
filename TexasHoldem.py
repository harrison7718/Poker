import random
from poker import Card
from Player import Player

class TexasHoldem(object):

  # initalize member variables
  def __init__(self, small_blind=1, big_blind=2):
    self.shuffle()                  # sets deck
    self.small_blind = small_blind  # small blind chip value
    self.big_blind = big_blind      # big blind chip value
    self.players = []               # list of players in game
    self.acting_player = Player()   # the player taking the next action
    self.acting_player_pos = 0      # position of the acting player in self.players 
    self.bb_pos = 0                 # position of the big blind
    self.sb_pos = 0                 # position of the small blind
    self.utg_pos = 0                # position of the under the gun
    self.last_better_pos = 0        # position of the starting better or the last player to bet 
    self.pot = 0                    # amount of chips in the pot
    self.bet = 0                    # size of the current bet
    self.board = []                 # list of cards visable on the table
    self.hand_over = False          # True if the hand is over and its time to start over

  # add a player to the game
  def addPlayer(self, player):
    self.players.append(player)

  # sets the next player to act
  def setNextActor(self):
    self.acting_player_pos += 1
    if self.acting_player_pos == len(self.players):
      self.acting_player_pos = 0
    self.acting_player = self.players[self.acting_player_pos]

  def makeBet(self, bet):
    # if the player has enough chips to make the bet
    if ( self.acting_player.chips >= bet - self.acting_player.bet ):
      self.bet = bet
      self.acting_player.chips -= (bet - self.acting_player.bet)
      self.pot += (bet - self.acting_player.bet)
      self.acting_player.stake += (bet - self.acting_player.bet)
      self.acting_player.bet = bet
      self.last_better_pos = self.acting_player_pos
      return True
    else:
      print('insuficiant funds!')
      return False

  def check(self):
    # if the player has enough chips to make the bet
    if ( self.acting_player.chips >= self.bet - self.acting_player.bet ):
      self.acting_player.chips -= (self.bet - self.acting_player.bet)
      self.pot += (self.bet - self.acting_player.bet)
      self.acting_player.stake += (self.bet - self.acting_player.bet)
      self.acting_player.bet = self.bet
      return True
    else:
      self.pot += self.acting_player.chips
      self.acting_player.stake += self.acting_player.chips
      self.acting_player.chips = 0
      return True

  # starts a betting round
  def playBettingRound(self):
    print('--- starting betting round ---')
    betting = True
    self.acting_player_pos = self.utg_pos
    self.acting_player = self.players[self.acting_player_pos]
    self.last_better_pos = self.acting_player_pos

    while betting:
      print(self)

      if self.acting_player.active and self.acting_player.chips > 0:

        action = ''

        while not action in ['c', 'b', 'f']:

          print('    ' + self.acting_player.name + '\'s turn')
          print('c to check/call, b to bet/raise, f to fold')
          action = input('c, b, or f? ')
          
          if action == 'c':
            self.check()
          elif action == 'b':
            bet = int(input('how many chips do you want to bet/raise to? \nbet = '))
            if not self.makeBet(bet):
              print('must make valid bet')
              action = ''
          elif action == 'f':
            self.acting_player.active = False
          else:
            print('must choose c, b, or f!')

      self.setNextActor()
      if (self.last_better_pos == self.acting_player_pos):
        betting = False

    # reset bets for next round & checks for a winner
    self.bet = 0
    active_players = 0
    winner = None
    for player in self.players:
      player.bet = 0
      if player.active:
        active_players += 1
        winner = player

    # if there is only one player active, they take the pot
    if active_players == 1:
      print(winner.name, 'wins', self.pot, 'chips!')
      winner.chips += self.pot
      self.pot = 0
      self.hand_over = True

  def showdown(self):
    print('showdown')

  # initalizes a single hand from start to finish
  def startHand(self):
    print('--- starting hand ---')
    self.shuffle()

    # Deal cards to each player
    for player in self.players:
      player.cards.append(self.deck.pop())
      player.cards.append(self.deck.pop())
    
    # PreFlop Bets
    self.playBettingRound() 

    # Flop
    if not self.hand_over:
      self.board.append(self.deck.pop())
      self.board.append(self.deck.pop())
      self.board.append(self.deck.pop())
      self.playBettingRound() 

    # Turn
    if not self.hand_over:
      self.board.append(self.deck.pop())
      self.playBettingRound() 

    # River
    if not self.hand_over:
      self.board.append(self.deck.pop())
      self.playBettingRound() 
      self.showdown()

  # sets deck to a full, shuffeled deck
  def shuffle(self):
    self.deck = list(Card)
    random.shuffle(self.deck)

  # protocal for printing the game
  def __repr__(self):
    repr = '--- Texas Hold\'em ---\n'
    repr += str(self.board) + '\n'
    repr += 'pot = ' + str(self.pot) + ': bet = ' + str(self.bet) + '\n' 

    for player in self.players:
      if player.active:
        repr += '    ' + player.name + ': chips = ' + str(player.chips) + ', bet = ' + str(player.bet)
      else:
        repr += '    ' + player.name + ': chips = ' + str(player.chips) + ', FOLDED'
      repr += '\n'
    
    return repr