
import random


class Player(object):
    '''  Represents a player with a name, balance, and current bet'''
    def __init__(self, name, balance = 50, bet = 0):
        name = name[0].upper() + name[1:].lower() #capitalize just first leter, assuming str(name) correctly formatted
        self.name = name
        self.balance = balance
        self.bet = bet

    def __str__(self):
        return self.name+': Balance $'+ str(self.balance)
    
    def __repr__(self):
        return self.name

    def __hash__(self):
        return hash(self.name)

    def get_name(self): 
        return self.name
    
    def get_balance(self):
        return self.balance
    
    def get_bet(self):
        return self.bet

    def make_bet(self, bet):
        self.bet = bet
        self.balance -= self.bet #takes it out of player account once bet is in
    
    def lose_bet(self):
        self.bet = 0
        print('Your new balance is {self.balance}')

    def win_bet(self, multiplier=1):
        winnings = self.bet*(1 + multiplier) #original bet plus winnings 
        self.balance += winnings
        self.bet = 0 #reset bet
        print('Your new balance is {self.balance}')

    def keep_bet(self):
        self.balance += self.bet
        self.bet = 0
        print('Your new balance is {self.balance}')


class Card(object):
    '''
    Represents card object with name & suit, as strings
    value: int for calculation, tuple for Ace
    '''
    def __init__(self, name, suit, value, visibility=1):
        self.name = name
        self.suit = suit
        self.value = value
        self.visibility = visibility #1 for on, 0 for off

    def get_value(self):
        return self.value
    
    def set_visibility_off(self):
        self.visibility = 0

    def set_visibility_on(self):
        self.visibility = 1

    def __str__(self):
        return self.name + ' of ' + self.suit #ex: Ace of Spades, King of Hearts
        
    def __repr__(self):
        if self.name == '10':
            return (self.name + self.suit[0]) 
        else: 
            return (self.name[0] + self.suit[0]) #ex: AS, KH


class Hand(Card):
    ''' 
    Represents a list of cards, with a bet value, and an total int value for calcs. 
    Uses str method to control what user sees.
    '''

    def __init__(self, bet):
        self.cards = []
        self.bet = bet
        self.value = 0
    
    def add_card(self, card):
        ''' Adds Card obj to list and recalculates hand val '''
        self.cards.append(card)
        self.value += card.get_value()
        # if self.value > 21:
        #     self.value = None

    def get_hand_val(self):
        return self.value
   
    def show_hand_partial(self):
        """ Returns list """
        res = []
        for card in self.cards:
            if card.visibility == 0:
                res.append('[]')
            else: res.append(card.get_name())
        return res

    def show_hand_all(self):
        """ Returns list """
        res = []
        for card in self.cards:
            res.append(card.get_name())    
        return res + f'    total_value = {self.value}'

    def __str__(self):
        res = []
        for card in self.cards:
            res.append(repr(card))
        res = ', '.join(res)

        if self.value <= 21:
            return res 
        else: return res + '   BUST'

    def __repr__(self):
        res = []
        for card in self.cards:
            res.append(repr(card))
        ','.join(res)
        return res


class Deck(object):
    '''
    Represents 
    1) reference list of all card objects, 
    2) Copy list to be shuffled and drawn from
    '''
    def __init__(self):
        self.ref_deck = []

        card_names = ['1','2','3','4','5','6','7','8','9','10','Jack','Queen','King','Ace']
        card_vals = [1,2,3,4,5,6,7,8,9,10,10,10,10,10]

        suits = ['Hearts','Diamonds','Clubs','Spades']
        for suit in suits:
            for i in range(len(card_names)):
                self.ref_deck.append(Card(card_names[i], suit, card_vals[i])) 
        
        self.deck = self.ref_deck.copy()
                
    def new_shuffle(self): ##still debating if this is the best way to do this...##
        '''returns shuffled list of all Card objects '''
        random.shuffle(self.deck)
        print("Deck has been shuffled.")
        return self.deck
  
    def __str__(self): #to print the whole deck, i.e. check shuffle
        res = []
        for card in self.deck:
            res.append(repr(card)+', \n')
        return res

  
#################
#################        


def build_players_list(players_list):
    '''
    - Takes input from users, builds list with up to max # of players
    - returns list containing all player objects
    '''
    
    # stop = False
    # while len(players_list) < 2 and stop == False: ##change max game size here##
    #     if len(players_list) == 0:
    #         while True:
    #             try: 
    #                 name = str(input("Enter 1st player name, or enter '*' to quit game: "))
    #                 break
    #             except: pass
    #     else: 
    #         while True:
    #             try: 
    #                 name = str(input("Enter next player name, or enter '*' to stop adding players: "))
    #                 break
    #             except: pass
    for name in ['Kev', 'dyl', '*']: ###prefilled
        if name in players_list or name == 'House':
            print('Name already chosen.')
        elif name == '*':
            break
        else: 
            player = Player(name)
            players_list.append(player) 
            print(f'Hello and welcome {player.get_name()}, your starting balance is $50.')
        
    return players_list


def check_keep_playing(players_list, balance_snapshot):
    '''
    Asks each player if they want to play again.
    Reports their results in turn,
    Returns whos playing next as list of player obj
    '''
    iteration_list = players_list.copy()
    for player in iteration_list: #reports score and asks to play again, removes players not playing
        ref_balance = balance_snapshot[player] #balance before this round started
        balance = player.get_balance()  #current balance
        name = player.get_name()
        win_amt = balance - ref_balance #positive int for winnings
        
        if balance > ref_balance: 
            win_or_lose = f'Won ${win_amt} this round!'
        elif balance == ref_balance: 
            win_or_lose = 'broke even.'
        elif balance < ref_balance: 
            loss = abs(win_amt)
            win_or_lose = f'lost ${loss} this round...'

        print(f'{name}, You {win_or_lose}')

        try: ##ADD FUNCTION HERE## for better input control, same for name choosing.
            ans = input('Keep Playing? (y/n)')
            try: ans.lower().strip()
            except: pass

            if ans == 'y' or ans == 'yes': 
                print(f'{name}, your starting balance will be ${player.get_balance()}.')
                #continues to next player

            elif ans == 'n' or ans == 'no': #if not playing again, $$ donated back to house
                if balance == 0:
                    print('Sorry to see you go, thanks for playing!')
                else: 
                    print(f'Sorry to see you go thanks for the ${balance}!')
                players_list.remove(player)
                #continues to next player

        except: print("I'll just pretend I understood that, you will play again") 
    
    if len(players_list) < 2:
        build_players_list(players_list)

    return players_list


def take_bet(player):
    ''' Takes in Player obj
    Processes user input to only allow integer bets within the acceptable range 0->Bal 
    Edits Player.bet attribute & returns bet as int
    '''
    while True:
        try:
            bet = int(input(f"{player}: Enter a bet, in increments of $1. Enter 0 to skip this hand.\n")) 
            if bet > balance: 
                try: bet = int(input('Enter a bet you can afford...'))
                except: pass
            elif bet < 0: 
                bet = abs(bet)
                print('Ha Ha. Very Funny.')
            else: break #balance is int within the acceptable range

        except:
            print(f"Must be a whole number that is less than or equal to your balance, ${player.get_balance()}")
            pass #keeps looping while incorrect input type

    player.make_bet(bet) #saves bet (pulls from player bal)
    print(f'${bet} from {player.get_name()}')
    return bet


def player_turn(table): 
    '''
    Takes everything on the table as dict, after the deal. Checks for dealer blackjack 
    Processes user input to determine end value and bets for each hand, returns updated table dict. 
    Hands with blackjack or bust should be excluded from further actions.
    '''
    dealers_hand = table['House']
    dealers_score = dealers_hand.get_hand_val()

    if dealers_score == 21: #checks for dealer blackjack
        for player in table: #check everyone else for blackjack
            if player.get_name()=='House': continue
            hand_val = table[player].get_hand_val() #no splits yet
            if hand_val < 21:
                player.lose_bet()
            elif hand_val == 21:
                player.keep_bet()
    
    for player in table.keys():
        if player.get_name() == 'House': continue
        hand = table[player]
        hand_val = hand.get_hand_val()
        print(f'{player.get_name()}: Your hand is {hand.show_hand_all} and the table shows as follows:')
        for key in table.keys():
            print(f'{player.get_name()}:',table[key].show_hand_partial())



def dealers_turn(table):
    '''
    Takes dict input for whole table, hit as necessary, and returns updated table dict
    '''


def score_table(table):
    '''
    compares cards from 'House' as ref. updates player bets based on win or loss.
    '''



def play_blackjack(players_list):
    '''
    Starts a new game, repeats until no bets placed or 'quit' command entered
    Returns players_list when done
    '''
    deck = Deck().new_shuffle()
    print(deck)
    table = {Player('House',1000):Hand(0)} #dict of player: Hand(bet) pairs, will replace Hand with list of Hands for splits, and handle errors dwnstream
    for player in players_list:
        if player.get_name() == 'House': continue
        take_bet(player) #assures bet is within acceptable range & edits player attribute
        table.update({player:Hand(player.get_bet())}) #creates new hand with player bet
    
    ##start of deal phase
    i=0 
    while i<2:
        for player in table.keys():
            if i == 1: #2nd card
                deck[0].set_visibility_off()
            table[player].add_card(deck.pop(0)) #deal top card one at a time each player gets 2
        i+=1
    
    #player turn
    for key in table.keys():
        name = key.get_name()
        hand = table[key]
        print (f'{name}:', hand)
    
    pass

    table = player_turn(table)

    #dealer turn
    table = dealers_turn(table)

    # if table('House').get_balance() <= 0: #if House runs out of money, users win maybe get to read a txt file backstory or something

    ##print ("Table:", repr(table)) #debugging

    #deal cards
    
    #for player in players_list:
        #deal until stop or bust, with option to split if same faced card
    
    
   



#################
#################


if __name__ == "__main__":
    keep_playing = True
    print("WELCOME TO BLACKJACK")
    players_list = build_players_list([]) #passes in empty list to start game
    table = players_list.copy()
    table.append(Player('House',1000)) #to include dealer 

    while keep_playing == True: #Keeps playing until bets stop
        balance_snapshot = {} 
        for player in players_list: #captures dict snapshot before playing
            balance = player.get_balance()
            balance_snapshot.update({player:balance})

        play_blackjack(table) #deals to players and dealer, changes player balances, repeats until no bets given

        players_list = check_keep_playing(table, balance_snapshot) #edits&returns players list based on who wants to keep playing, any leftover money is donated back to house...naturally.

        if len(players_list) == 0: #exit program when empty table
            print('Bye for now!')
            keep_playing = False
        else: 
            playing = []
            for x in players_list: playing.append(str(x))
            if len(playing) > 1: print(f'Starting new game with {playing[:-1]} and {playing[-1:]}')
            else: print(f'Starting new game with {playing}.')
            