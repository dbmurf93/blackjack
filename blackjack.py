
import random


class Player(object):
    '''  Represents a player with a name, balance, and current bet'''
    def __init__(self, name, balance = 50, bet = 0):
        name = name[0].upper() + name[1:].lower() #capitalize just first leter, assuming str(name) correctly formatted
        self.name = name
        self.balance = balance
        self.bet = bet

    def __str__(self):
        return self.name
    
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
    Represents card object with name & suit, as str
    value: int for calculation, Aces 10 by default with alt handled in scoring function of Hand
    '''
    def __init__(self, name, suit, value, visibility=1):
        self.name = name
        self.suit = suit
        self.value = value
        self.visibility = visibility #default 1 for on, 0 for off

    def get_value(self):
        return self.value
    
    def get_card_name(self):
        return self.name

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

    def __init__(self, bet, card = None):
        self.cards = []
        if card != None: self.cards.append(card)
        self.bet = bet
    
    def add_card(self, card):
        ''' Adds Card obj to list and recalculates hand val '''
        self.cards.append(card)

    def get_hand_val(self):
        value = 0
        for card in self.cards:
            value += card.get_value()
        return value
    
    def get_bet(self):
        return self.bet
    
    def show_hand_partial(self):
        """ Returns list """
        res = []
        for card in self.cards:
            if card.visibility == 0:
                res.append('[]')
            else: res.append(str(card))
        return res

    def show_hand_all(self):
        """ Makes all cards visible, Returns formatted list """
        res = []
        for card in self.cards:
            res.append(str(card)) 
            card.set_visibility_on() #flips over card once viewed   
        res = ', '.join(res)
        return res + f'    total_value = {self.get_hand_val()}'

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


class Deck(Card):
    '''
    Represents 
    1) reference list of all card objects, 
    2) Copy list to be shuffled and drawn from
    '''
    def __init__(self):
        self.ref_deck = []
        self.deck = []

        card_names = ['2','3','4','5','6','7','8','9','10','Jack','Queen','King','Ace']
        card_vals = [2,3,4,5,6,7,8,9,10,10,10,10,11]

        suits = ['Hearts','Diamonds','Clubs','Spades']
        for suit in suits:
            for i in range(len(card_names)):
                self.ref_deck.append(Card(card_names[i], suit, card_vals[i])) 
        
        self.new_shuffle()
    
    def new_shuffle(self): 
        '''shuffles self.deck in place, returns list '''
        self.deck = self.ref_deck.copy()
        random.shuffle(self.deck)
        print("Deck has been shuffled.")
  
    def __str__(self): #to print the whole deck, i.e. check shuffle
        res = []
        for card in self.deck:
            res.append(repr(card)+', \n')
        return res
    
    def draw_card(self):
        '''Returns top card from deck and removes from stack '''
        return self.deck.pop(0)

    def draw_card_facedown(self):
        self.deck[0].set_visibility_off()
        return self.deck.pop(0)


class Table(object):
    """ 
    Represents a dict of players: hands
    stores Deck obj
    passed in and out of f'n args to keep current 
    """ 
    
    def __init__(self, table_dict, deck):
        self.table_dict = table_dict
        self.deck = deck

    def get_dict(self):
        return self.table_dict
    
    def __str__(self):
        return self.table_dict #defers to player and hand repr methods


##################
##################       


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

def check_funds(player, amt):
    ''' Returns True for acceptable bets, false for negative or too high '''
    bal = player.get_balance()
    if 0 > bal > amt:
        return False
    elif 0 >= bal >= amt:
        return True

def take_bet(player):
    ''' 
    Takes in Player obj
    Processes user input to only allow integer bets within the acceptable range 0->Bal 
    Edits Player.bet attribute & returns updated player obj
    '''
    while True: #input control loop
        try:
            balance = player.get_balance()
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
    print(f'${bet} from {player.get_name()}') #confirm bet
    return player

def table_view(player, table):
    '''
    Represents a player looking at the rest of the table (some cards will be face down)
    Takes table obj and maps Hands to names instead of Player obj
    for print
    '''
    table_dict = table.table_dict
    for key in table_dict.keys(): #looks at each player&house 
        if key.get_name() == player.get_name(): continue #skip self
        print(f'{key}: {table_dict[key].show_hand_partial()}')

def balance_snapshot(table):
    ''' captures dict snapshot of players' balances for later reporting. Returns dict '''
    balance_snapshot = {} 
    for player in table: 
        if player.get_name() == 'House': continue 
        bal = player.get_balance()
        balance_snapshot.update({player:bal}) #save point for later comparison
    
    return balance_snapshot

def deal_cards(table):
    ''' takes Table obj, deals 1up1dwn to each seat, returns updated table. '''
    i=0 
    table_dict = table.table_dict
    while i<2:
        for player in table_dict.keys():
            if i == 1: #2nd card 
                table_dict[player].add_card(table.deck.draw_card_facedown())#dealt face down
            else: 
                table_dict[player].add_card(table.deck.draw_card()) #deal top card one at a time each player gets 2
        i+=1
    return table



def split_hand(player, bet, hand, table):
    ''' splits hand, updates player balance for new bet, returns updated table '''
    hand1 = Hand(bet, hand.cards[0]) #breaks out indiv. cards
    player.make_bet(bet) #dbls player bet
    hand2 = Hand(bet, hand.cards[1])
    if type(table[player]) == list: #"if there's already been a split"
        table[player].append(hand1)
        table[player].append(hand2) 
    else: table.update({player:[hand1,hand2]}) #overwrites Hand obj to list with 2 single card hands 

    return table

def hitorstick(player, hand, table):
    ''' prompts user until exit or bust, changes player and hand, & returns updated table '''
    
    while keep_playing: # loop operates on player and hand before adding to table 
        print (f'{player}, Your hand is {hand.show_hand_all()}.')
        print(f'{player}: Enter "H" to hit for another card, or "*" to stick with your current hand')
        ans = str(input("(H / *)  :   ")).lower()
        if ans ==  'h':
            hand.add_card(table.deck.draw_card()) #pull card from the deck and add to player hand

        elif ans == '*':
            print(f'{player} chooses to stand at {hand.get_hand_val()}.')
            break
        if hand.get_hand_val() > 21:
            print (f'{player}, Your hand is {hand.show_hand_all()}.')
            print ('Ah shoot, bust!')


    table.table_dict.update({player:hand}) #overwrites info at slot
    return table

def play_hand(player, hand, table):
    ''' Shows players cards, partial view dict, & takes action as directed, returns updated table '''
    table_dict = table.table_dict
    hand = table_dict[player]
    try:
        for i in hand: #catches when split hands are passed in
            table = play_hand(player, i, table) #plays em individually
    
    except(TypeError): #for when single hand objs passed in
        print(f'{player.get_name()}: Your hand is {hand.show_hand_all()} and the table shows as follows:')
        table_view(player, table) #prints table from player POV
        
        #if split is possible..
        if hand.cards[0].get_card_name() == hand.cards[1].get_card_name(): 
            bet = hand.get_bet()
            if check_funds(player, bet): #proceeds if player has enough to split
                print('Would you like to split your hand?')
                ans = str(input('Enter "s" to split.\n')).lower()
                if ans == 's':
                    table = split_hand(player, bet, hand, table) #updates table with new player hand-list
            else: #not enough funds to split
                pass 

        table = hitorstick(player, hand, table)
            
    
    return table




def all_player_turns(table): 
    '''
    Takes in Table obj. Checks for dealer blackjack 
    Processes user input to determine bets for each hand, returns updated table dict. 
    **Hands with 21+ should be excluded from further actions.
    '''
    table_dict = table.table_dict
    for key in table_dict.keys():
        if key.get_name() == 'House':
            housekey = key  #cleaner way to get this key???
    dealers_hand = table_dict[housekey]
    dealers_score = dealers_hand.get_hand_val()
    
    ##checking for dealer blackjack 1st
    if dealers_score == 21: 
        for player in table_dict: #check everyone else for blackjack
            if player.get_name()=='House': continue
            hand_val = table[player].get_hand_val() #no splits yet
            if hand_val < 21:
                player.lose_bet()
            elif hand_val == 21:
                player.keep_bet() #$ back into player balance
   
    ##player turn start
    for player in table_dict.keys():
        if player.get_name() == 'House': continue #skips 
        hand = table_dict[player]
        table = play_hand(player, hand, table) #player chooses to add cards, split, and when to stop if no bust

    return table

def dealers_turn(table):
    '''
    Takes dict input for whole table, hit as necessary, and returns updated table dict & deck
    '''
    return table

def score_table(table):
    '''
    compares cards from 'House' as ref. updates player bets based on win or loss.
    '''
    pass




def setup_table(players_list):
    ''' Adds players and house to seats with empty hands, adds bets to each hand, and returns table '''
    table_dict = {Player('House',1000):Hand(0)} #dict of player: Hand(bet) pairs, planning to replace Hand with list of Hands for splits, and handle errors dwnstream
    
    #gather bets
    for player in players_list: 
        if player.get_name() == 'House': continue
        player = take_bet(player) #assures bet is within acceptable range & edits player attribute
        if player.get_bet() > 0:
            table_dict.update({player:Hand(player.get_bet())}) #creates new hand with player bet

         #create Table object, highest level container
    table = Table(table_dict, Deck())
    return table

def play_blackjack(players_list):
    '''
    Plays multiple hands, Changes player balances accordingly, repeats until no bets or stop command given
    Returns updated players_list on exit
    '''
    stop = False
    while stop == False:
        ##Table setup    
        table = setup_table(players_list)

        ##dealing 2 cards to all seats
        table = deal_cards(table)

        # if check_dealer_blackjack(table):
        #     break
        
        #players' turns
        table = all_player_turns(table) #returns updated table when done

        #dealer's turn
        table = dealers_turn(table) 

        
    #adjust player balances based on hands in comparison to dealer
    table = score_table(table)
    return table
        
        
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

   
#################
#################


if __name__ == "__main__": 
    keep_playing = True
    print("WELCOME TO BLACKJACK")

    table = build_players_list([]) #passes in empty list to start game
    table.append(Player('House',1000)) #to include dealer 

    while keep_playing == True: #Keeps playing until bets stop
        #beginning of a "round" (contains multiple hands dealt)
        balance_snapshot = balance_snapshot(table)

        table = play_blackjack(table) 

        players_list = check_keep_playing(table, balance_snapshot) #edits&returns players list based on who wants to keep playing, any leftover money is donated back to house...naturally.

        if len(players_list) == 1: #exit program when empty table except house
            print('Bye for now!')
            keep_playing = False

        elif len(players_list) > 1: 
            print(f'Starting new game with {players_list[:-1]} and {players_list[-1:]}')
            
        else: print(f'Starting new game with {players_list}.')
            