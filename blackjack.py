### Welcome to blackjack, 
### facilities are under construction, 
###avoid bringing loved ones onto premises

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

    def __eq__(self, other):
        return self.name == other

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
        loss = self.bet
        self.bet = 0
        if self.balance != 0:
            print(f'{self.name} you lost {loss}....Your new balance is ${self.balance}')
        else: print('You lost everything....')

    def win_bet(self, multiplier=1):
        winnings = self.bet*(1 + multiplier) #original bet plus winnings 
        self.balance += winnings
        self.bet = 0 #reset bet
        print(f'{self.name} you won {winnings}! Your new balance is {self.balance}')

    def keep_bet(self):
        self.balance += self.bet
        self.bet = 0
        print(f'{self.name} you broke even. Your new balance is {self.balance}')

    def take_bet(self):
        ''' 
        Processes user input to only allow integer bets within the acceptable range 0->Bal 
        Edits Player.bet attribute & updates player obj
        '''
        while True: #input control loop
            try:
                balance = self.balance
                bet = int(input(f"{self.name}: Enter a bet, in increments of $1. Enter 0 to skip this hand.\n")) 
                if bet > balance: 
                    try: bet = int(input('Enter a bet you can afford...'))
                    except: pass
                elif bet < 0: 
                    bet = abs(bet)
                    print('Ha Ha. Very Funny.')
                else: break #balance is int within the acceptable range

            except:
                print(f"Must be a whole number that is less than or equal to your balance, ${self.balance}")
                pass #keeps looping while incorrect input type

        self.make_bet(bet) #saves bet (pulls from player bal)
        print(f'${bet} from {self.name}\n') #confirm bet
        return bet

    def check_funds(self, amt):
        ''' Returns True for acceptable bets, false for negative or too high '''
        bal = self.balance
        if 0 > bal > amt:
            return False
        elif 0 >= bal >= amt:
            return True



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

    def get_value(self):
        return self.value
    
    def get_card_name(self):
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

def adjust_for_ace(hand): ##TODO
    pass



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

    def deal_cards(self):
        ''' takes Table obj, deals 1up1dwn to each seat, updates table. '''
        i=0 
        table_dict = self.table_dict
        while i<2:
            for player in table_dict.keys():
                if i == 1: #2nd card 
                    table_dict[player].add_card(self.deck.draw_card_facedown())#dealt face down
                else: 
                    table_dict[player].add_card(self.deck.draw_card()) #deal top card one at a time each player gets 2
            i+=1
        print("Dealing complete\n")

    def deal_cards_for_testing(self):
        ''' 
        test iterations to check:
        1)deal everyone a split hand,
        2)deal dealer blackjack 
        
        test iterations completed:
        none
        '''
        for player in self.table_dict.keys():
                self.table_dict[player].add_card(Card('7','Hearts',7))
                self.table_dict[player].add_card(Card('7','Clubs',7)) #deal top card one at a time each player gets 2

        print("Testing Deal complete\n")

    def all_player_turns(self): 
        '''
        Takes in Table obj. Checks for dealer blackjack 
        Processes user input to determine bets for each hand, updates table dict. 
        **Hands with 21+ should be excluded from further actions.
        '''
        table_dict = self.table_dict
        
        dealers_hand = table_dict['House']
        dealers_score = dealers_hand.get_hand_val()
        
        ##checking for dealer blackjack 1st
        if dealers_score == 21: 
            for player in table_dict: #check everyone else for blackjack
                if player =='House': continue
                hand_val = table_dict[player].get_hand_val() #no splits yet
                if hand_val < 21:
                    player.lose_bet()
                elif hand_val == 21:
                    player.keep_bet() #$ back into player balance
    
        ##player turn start
        for player in table_dict.keys():
            if player == 'House': continue #skips 
            hand = table_dict[player]
            table.play_hand(player, hand) #player chooses to add cards, split, and when to stop if no bust
     
    def table_view(self, player):
        '''
        Represents a player looking at the rest of the table (some cards will be face down)
        Takes table obj and maps Hands to names instead of Player obj
        for print
        '''
        for key in self.table_dict.keys(): #looks at each player&house 
            if key == player: continue #skip self
            print(f'{key}: {self.table_dict[key].show_hand_partial()}')

    def play_hand(self, player, hand):
        ''' Shows players cards, partial view dict, & takes action as directed, updates table '''
        table_dict = self.table_dict
        hand = table_dict[player]
        try:
            for h in hand: #catches when split hands are passed in
                self.play_hand(player, h) #plays em individually
        
        except(TypeError): #for when single hand objs passed in
            print(f'\n\n{player.get_name()}: The table shows as follows:')
            table.table_view(player) #prints table from player POV
            
            #if split is possible..
            print(hand.cards[0].get_name())
            print(hand.cards[1].get_name())

            if hand.cards[0].get_card_name() == hand.cards[1].get_card_name(): 
                bet = hand.get_bet()
                if player.check_funds(bet): #proceeds if player has enough to split
                    print('Would you like to split your hand?')
                    ans = str(input('Enter "s" to split.\n')).lower()
                    if ans == 's':
                        self.play_split_hand(player, bet, hand) #updates table with new player hand-list
                else: #not enough funds to split
                    pass 

            table.hitorstick(player, hand) #passes in hand in question, not sure this avoids playing a hand twice
                
        
        return table

    def play_split_hand(self, player, bet, hand):
        ''' splits hand, updates player balance for new bet, updates table '''
        hand1 = Hand(bet, hand.cards[0]) #breaks out indiv. cards
        player.make_bet(bet) #dbls player bet
        hand2 = Hand(bet, hand.cards[1])
        if type(table[player]) == list: #"if there's already been a split"
            self.table_dict[player].append(hand1)
            self.table_dict[player].append(hand2) 
        else: self.table_dict.update({player:[hand1,hand2]}) #overwrites Hand obj to list with 2 single card hands 

    def hitorstick(self, player, hand):
        ''' prompts user until exit or bust, changes player and hand, & updates table '''
        
        while True: # loop operates on player and hand before adding to table 
            print (f'Your hand is {hand.show_hand_all()}.')
            print(f'{player}: Enter "H" to hit for another card, or "*" to stick with your current hand')
            ans = str(input("(H / *)  :   ")).lower()
            if ans ==  'h':
                hand.add_card(self.deck.draw_card()) #pull card from the deck and add to player hand

            elif ans == '*':
                print(f'{player} chooses to stand at {hand.get_hand_val()}.\n\n')
                break
            if hand.get_hand_val() > 21:
                print (f'{player}, Your hand is {hand.show_hand_all()}.\nBUST!\n\n')
                break

        self.table_dict.update({player:hand}) #overwrites info at slot

    def dealers_turn(self):
        '''
        Takes dict input for whole table, hit as necessary, update info
        '''
        table_dict = self.table_dict
        
        while True:
            dealers_hand = table_dict['House']
            dealers_score = dealers_hand.get_hand_val()

            if 17 < dealers_score <= 21:
                print ('Dealer scores:', dealers_score)
                break #continue to scoring
            elif dealers_score <= 17:
                self.table_dict['House'].add_card(self.deck.draw_card())
            elif dealers_score > 21:
                print ("Dealer busts!")
                break

    def score_table(self):
        '''
        compares cards from 'House' as ref. updates player bets based on win or loss.
        '''
        dealers_hand = self.table_dict['House']
        dealers_score = dealers_hand.get_hand_val()
        td = self.table_dict
        for player in td:
            if player == 'House': continue
            score = td[player].get_hand_val()
            if score <= 21:
                if score > dealers_score: 
                    player.win_bet()

                elif score == dealers_score:
                    player.keep_bet()

                elif score < dealers_score and dealers_score <= 21:
                    player.lose_bet()

                elif score < dealers_score and dealers_score > 21:
                    player.win_bet() 
            else: 
                print (f'{player} Busted.')
                player.lose_bet()
   
    def balance_snapshot(self):
        ''' captures dict snapshot of players' balances for later reporting. Returns dict '''
        balance_snapshot = {} 
        for player in self.table_dict: 
            if player.get_name() == 'House': continue 
            bal = player.get_balance()
            balance_snapshot.update({player:bal}) #save point for later comparison
    
        return balance_snapshot

    def take_player_bets(self):
        ''' Goes around the table and creates hands with bets for players '''
        for player in self.table_dict: 
            if player == 'House': 
                self.table_dict.update({player:Hand(0)}) #set up empty hand for House
                continue #and skip to next player
            bet = player.take_bet() #assures bet is within acceptable range & edits player attribute
            if bet > 0:
                self.table_dict.update({player:Hand(player.get_bet())}) #creates new empty hand with player bet

    def play_blackjack(self):
        '''
        Plays multiple hands, Changes player balances accordingly, repeats until no bets 
        Returns updated players_list on exit
        '''
        stop = False
        while stop == False:
            self.take_player_bets() #breaks out if all non-house bets are 0
            if all(player.get_bet() == 0 for player in self.table_dict):
                break
            ##dealing 2 cards to all seats
            self.deal_cards()

            #players' turns
            self.all_player_turns() #returns updated table when done

            #dealer's turn
            self.dealers_turn() 

            #adjust player balances based on hands in comparison to dealer
            self.score_table()

         

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
        if player == 'House': continue
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
        build_players_list(players_list)  ##loops endlessly until 

    return players_list

def setup_table(players_list):
    '''set up new table object, empty table_dict & fresh deck, returns table object '''    
    table_dict = {} #dict of player: Hand(bet) pairs, planning to replace Hand with list of Hands for splits, and handle errors dwnstream
    #create Table object, highest level container, w/ new deck
    for player in players_list:
        table_dict.update({player:Hand(0)}) #empty spot for everyone
    table = Table(table_dict, Deck())

    return table
    
def build_players_list(players_list):
    '''
    - Takes input from users, builds list with up to max # of players
    - returns list containing all player objects
    '''
    while len(players_list) < 3:
        try:
            name = str(input("Choose your name."))
        except: pass #resets if user enters impossible str
        player = Player(name) #formats name str and creates obj
        if name in players_list or name == 'House':
            print ('Name already taken')
            continue

        elif name == '*':
            print('Done adding players.\n')
            break
        else:
            players_list.append(player) 
            print(f'Hello and welcome {player.get_name()}, your starting balance is $50.')
            
        
    return players_list

   
#################
#################


if __name__ == "__main__": 
    keep_playing = True
    print("WELCOME TO BLACKJACK")

    #pass in empty list and add dealer to table
    players_list = build_players_list([])
    players_list.append(Player('House',1000)) 

    while keep_playing == True: #Keeps playing until bets stop
        ##Table setup    
        table = setup_table(players_list) #sets up new Table obj, clears dict and takes bets

        #beginning of a "round" (contains multiple hands dealt)
        balance_snapshot = table.balance_snapshot()
        
        table.play_blackjack() 

        #and then after each "round"
        players_list = check_keep_playing(players_list, balance_snapshot) #edits&returns players list based on who wants to keep playing, any leftover money is donated back to house...naturally.

        
        if len(players_list) == 1: #exit program when empty table except house
            print('Bye for now!')
            keep_playing = False

        elif len(players_list) > 1: #otherwise spin back up 
            print(f'Starting new game with:')
            for player in players_list:
                if player == 'House': continue
                print (player)            
        
            