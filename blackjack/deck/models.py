from .utils import new_shuffle


class Card(object):
    '''
    Represents card object with name & suit, as str
    value: int for calculation, Aces 10 by default with alt handled in scoring function of Hand
    '''
    def __init__(self, name, suit, value, visibility=1):
        self.name = name
        self.suit = suit
        self.value = value
        self.visibility = visibility #default 1 for on, 0 for off

    def __str__(self):
        return self.name + ' of ' + self.suit #ex: Ace of Spades, King of Hearts
        
    def __repr__(self):
        if self.name == '10':
            return (self.name + self.suit[0]) 
        else: 
            return (self.name[0] + self.suit[0]) #ex: AS, KH

    def __eq__(self,other): #compares only front of repr string, excludes suit
        return repr(self)[:-1] == repr(other)[:-1] 

    def get_value(self):
        return self.value
    
    def get_name(self):
        return self.name

    def set_visibility_off(self):
        self.visibility = 0

    def set_visibility_on(self):
        self.visibility = 1


class Hand(Card):
    ''' 
    Represents a list of cards, with a bet value, and an total int value for calcs. 
    Uses str method to control what user sees.
    '''

    def __init__(self, bet, card = None):
        self.cards = []
        if card: 
            self.add_card(card)
        self.bet = bet
        self.completed = False

    def __str__(self):
        result = []
        for card in self.cards:
            result.append(repr(card))
        result = ', '.join(result)
        value = self.get_hand_val()
        if value == 21 and len(self.cards) == 2:
            return result + ' - BLACKJACK'
        elif value <= 21:
            return result 
        return result + '\nBUSTED!'

    def __repr__(self):
        res = []
        for card in self.cards:
            res.append(repr(card))

        res = ','.join(res)
        return res
    
    def add_card(self, card):
        ''' Adds Card obj to list and recalculates hand val '''
        self.cards.append(card)

    def get_hand_val(self):
        value = 0
        ace_ct = 0
        for card in self.cards:
            if card.get_name() == 'Ace': #count if Ace
                ace_ct += 1
            value += card.get_value()
        while ace_ct > 0: #skips for no Aces
            if value > 21:
                value -= 10 
                ace_ct -= 1
                if value > 21: continue #loop until value within range or aces used up
            else: break

        return value
    
    def get_bet(self):
        return self.bet
    
    def show_hand_partial(self):
        """ Returns visibility dependent list """
        res = []
        for card in self.cards:
            if card.visibility == 0:
                res.append('[]')
            else: res.append(repr(card))
        return res

    def show_hand_all(self):
        """ Makes all cards visible to everyone at the table, Returns formatted str """
        res = []
        for card in self.cards:
            res.append(str(card)) 
            card.set_visibility_on() #flips over card once viewed   
        res = ', '.join(res)
        return res + f' ->(total_value = {self.get_hand_val()})'

    def mark_completed(self):
        self.completed = True
        print ('Moving on...')

    def check_completed(self):
        return self.completed


class Deck(Card):
    '''
    Represents 
    1) reference list of all card objects, 
    2) Copy list to be shuffled and drawn from
    '''
    def __init__(self):
        self.ref_deck = []
        self.deck = []

        CARD_NAMES_VALUES = {
            '2':2,
            '3':3,
            '4':4,
            '5':5,
            '6':6,
            '7':7,
            '8':8,
            '9':9,
            '10':10,
            'Jack':10,
            'Queen':10,
            'King':10,
            'Ace':11,
        }

        suits = ['Hearts','Diamonds','Clubs','Spades']
        self.ref_deck.update([Card(name, suit, value) for suit in suits for name, value in CARD_NAMES_VALUES])

        new_shuffle(self)
  
    def __str__(self): #to print the whole deck, i.e. check shuffle
        res = []
        for card in self.deck:
            res.append(repr(card)+', \n')
        return res
    

