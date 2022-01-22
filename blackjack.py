### Welcome to blackjack, 
### we do not have a fancy README.md
### all requests for fancy accoutrements 
### will be rejected outright, with haste

import random
max_table_size = 4 #includes House 

class Player(object):
    '''  
    Represents a player with a name, balance, and current bet,
    was thinking could add an attribute for playing_status, and store player balance 
    so you cant just rest to get the starting $50
    '''
    def __init__(self, name, balance = 50, bet = 0):
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
        if self.balance != 0:
            print(f'{self.name} you lost ${loss}....Your new balance is ${self.balance}')
        else: print('You lost everything....')

    def win_bet(self, multiplier=1.):
        winnings = int(self.bet*(1 + multiplier)) #original bet plus winnings 
        self.balance += winnings #adjust plyr bal first
        winnings -= self.bet #subtract bet for print statement
        self.bet = 0 #reset plyr bet 
        print(f'{self.name} you won ${winnings}! Your new balance is ${self.balance}')

    def keep_bet(self):
        self.balance += self.bet
        self.bet = 0
        print(f'{self.name} you broke even. Your new balance is ${self.balance}')

    def take_bet(self):
        ''' 
        Processes user input to only allow integer bets within the acceptable range 0->Bal 
        Edits Player.bet attribute & updates player obj
        '''
        balance = self.balance
        while True: #input control loop
            try:
                bet = int(input(f"{self.name}: Enter a bet, in increments of $2. Enter 0 to skip this hand.\n")) 
                if bet % 2 != 0:
                    print('Must be an even number...')
                elif bet > balance: 
                    print('Enter a bet you can afford...')
                elif bet < 0: 
                    bet = abs(bet)
                    print('Ha Ha. Very Funny.')
                else: break #balance is int within the acceptable range

            except:
                print(f"Must be an even, whole number that is less than or equal to your balance, ${self.balance}")
                pass #keeps looping while incorrect input type

        self.make_bet(bet) #saves bet (pulls from player bal)
        print(f'${bet} from {self.name}\n') #confirm bet
        return bet

    def check_funds(self, amt):
        ''' Returns True for acceptable bets, false for negative or too high '''
        bal = self.balance
        if amt < 0 or amt > bal :
            return False
        elif amt <= bal or amt == 0:
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

    def __eq__(self,other): #compares only front of repr string, excludes suit
        return repr(self)[:-1] == repr(other)[:-1] 

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
        if card != None: self.add_card(card)
        self.bet = bet
        self.completed = False

    def __str__(self):
        res = []
        for card in self.cards:
            res.append(repr(card))
        res = ', '.join(res)

        if self.get_hand_val() == 21 and len(self.cards) == 2:
            return res + ' - BLACKJACK'
        elif self.get_hand_val() <= 21:
            return res 
        else: return res + '\nBUSTED!'

    def __repr__(self):
        res = []
        for card in self.cards:
            res.append(repr(card))

        res = ','.join(res)
        return res
    
    def add_card(self, card):
        ''' Adds Card obj to list and recalculates hand val '''
        self.cards.append(card)

    def get_hand_val(self): ##TODO add 'Blackjack!' string
        value = 0
        ace_ct = 0
        for card in self.cards:
            if card.get_card_name() == 'Ace': #count if Ace
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

        card_names = ['2','3','4','5','6','7','8','9','10','Jack','Queen','King','Ace']
        card_vals = [2,3,4,5,6,7,8,9,10,10,10,10,11]

        suits = ['Hearts','Diamonds','Clubs','Spades']
        for suit in suits:
            for i in range(len(card_names)):
                self.ref_deck.append(Card(card_names[i], suit, card_vals[i])) 
        
        self.new_shuffle()
    
    def new_shuffle(self): #self.deck shuffled on obj creation
        '''shuffles self.deck in place '''
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
    
    def __str__(self):
        return self.table_dict #defers to player and hand repr methods
       
    #####################

    def player_turn(self, player, hand_list): 
        '''
        Takes in list obj. 
        sends 1 Hand obj at a time into hit_or_stick 
        returns played_hands
        '''
        played_hands = []
        for hand in hand_list:
            if self.check_for_split(player, hand):
                plyd_hands = self.split_hand(player, player.get_bet(), hand) #returns 2 plyd hands
                for each in plyd_hands:
                    played_hands.append(each)
            else: 
                plyd_hand = self.hit_or_stick(player, hand) #passes in single hand object
                if plyd_hand != None: played_hands.append(plyd_hand)
    
        return played_hands
            
    def check_for_split(self, player, hand):
        ''' checks cards, checks player funds, asks player if appropriate, returns T/F '''
        ans='' #create empty var
        #if split is possible.. 
        if hand.cards[0] == hand.cards[1]: #only compares 'name'
            bet = hand.get_bet()
            if player.check_funds(bet): #proceeds if player has enough to split
                print (f'{player}, Your hand is {hand.show_hand_all()}.')
                print('Would you like to split your hand?')
                ans = str(input('Enter "S" to split.\n')).lower()

        if ans == 's':
            print ('splitting hand...')
            return True
        else: return False
                
    def split_hand(self, player, bet, hand):
        ''' input hand obj, breaks into list w two new obj, 
        updates player balance for new bet, overwrites self.table_dict '''
        
        hand1 = Hand(bet, hand.cards[0]) #breaks out indiv. cards
        hand1.add_card(self.deck.draw_card()) #and deals card to new split hand

        player.make_bet(bet) #dbls player bet edits player balance attr
        hand2 = Hand(bet, hand.cards[1])
        hand2.add_card(self.deck.draw_card())

        self.table_dict[player].pop()
        self.table_dict[player].append(hand1)
        self.table_dict[player].append(hand2)
        played_hands = self.player_turn(player, [hand1,hand2])
        
        return played_hands
        
        
    
    def table_view(self, player):
        '''
        Represents a player looking at the rest of the table (some cards will be face down)
        Takes table obj and maps Hands to names instead of Player obj
        for print
        '''
        for key in self.table_dict.keys(): #looks at each player&house 
            res = []
            # if key == player: continue #skip self #skipped for debugging but I like the look
            try: 
                for hand in self.table_dict[key]:
                    res.append(hand.show_hand_partial())
            except: 
                print(f"issue printing {player}'s hand")
            print(f'{key}: {res}')
        print('\n')
       
    def hit_or_stick(self, player, hand):
        ''' prompts user until exit or bust, changes player and hand, & updates table '''
        if hand.check_completed() == False: #skips completed hands
            while True: # loop operates on player and hand before adding to table 
                print ('Table shows:')
                if hand.get_hand_val() == 21 and len(hand.cards) == 2:
                    print (f'Your hand, {player}, is {hand.show_hand_all()}.')
                    print("Blackjack!! Winner winner chicken dinner")
                    break
                self.table_view(player)
                print (f'Your hand, {player}, is {hand.show_hand_all()}.')
                print(f'{player}: Enter "H" to hit for another card, or "*" to stick with your current hand')
                ans = str(input("(H / *)  :   ")).lower().strip()
                if ans ==  'h':
                    hand.add_card(self.deck.draw_card()) #pull card from the deck and add to player hand

                elif ans == '*':
                    print(f'{player} chooses to stand at {hand.get_hand_val()}.\n\n')
                    break
                if hand.get_hand_val() > 21:
                    print (f'{player}, Your hand is {hand.show_hand_all()}. - BUST!\n\n')
                    break
            hand.mark_completed()
            return hand
        else: return None

        
    #####################

    def dealers_turn(self):
        '''
        if no blackjack, hit as necessary, update self
        '''
        table_dict = self.table_dict
        while True:
            dealers_hand = table_dict['House'][0]
            dealers_score = dealers_hand.get_hand_val()

            if 17 < dealers_score <= 21:
                print ('Dealer scores:', dealers_score)
                break #continue to scoring
            elif dealers_score <= 17:
                print ('Dealer takes a card..')
                self.table_dict['House'][0].add_card(self.deck.draw_card())
                print ('New hand =', self.table_dict['House'])
            elif dealers_score > 21:
                print ("Dealer busts!")
                break
        
    def score_table(self):
        '''
        compares cards from 'House' as ref. updates player bets based on win or loss.
        '''
        dealers_hand = self.table_dict['House'][0]
        dealers_score = dealers_hand.get_hand_val()
        print ('\nScoring:')
        for player in self.table_dict.keys():
            if player == 'House': continue
            for hand in self.table_dict[player]:
                score = hand.get_hand_val()
                if score <= 21:
                    if score == 21 and len(hand.cards)==2:
                        player.win_bet(1.5)
                        
                    elif score > dealers_score: 
                        player.win_bet()

                    elif score == dealers_score:
                        player.keep_bet()

                    elif score < dealers_score and dealers_score <= 21:
                        player.lose_bet()

                    elif dealers_score > 21:
                        player.win_bet() 
                    
                else: 
                    print (f'{player} Busted.')
                    player.lose_bet()
   
    #####################

    def take_player_bets(self):
        ''' Goes around the table and overwrites new hands with bets for players '''
        for player in self.table_dict: 
            hand_list = []
            self.table_dict.update({player:hand_list}) #start w clean slate

            if player == 'House': 
                hand_list.append(Hand(0))
                self.table_dict.update({player:hand_list}) #set up empty hand for House
                continue #and skip to next player
            
            bet = player.take_bet() #assures bet is within acceptable range & edits player attribute
            if bet > 0:
                hand_list.append(Hand(bet))
                self.table_dict.update({player:hand_list}) #overwrites to player's hand list

    def deal_cards(self):
        ''' takes Table obj, deals 1up1dwn to each seat, updates table. '''
        for player in self.table_dict.keys():
            i=0 
            if player.get_bet() == 0 and player != 'House': continue
            new_hand = [Hand(player.get_bet())]
            while i<2:
                if i == 1: #2nd card 
                    card = self.deck.draw_card_facedown()
                    new_hand[0].add_card(card)#dealt face down
                else: 
                    card = self.deck.draw_card()
                    new_hand[0].add_card(card) #deal top card one at a time each player gets 2
                i+=1 #cards-dealt counter
            self.table_dict[player] = new_hand

        print("Dealing complete\n")

    def deal_cards_for_testing(self):
        ''' 
        test iterations will be really important for debugging bigger stuff
        '''
        i = 0
        for player in self.table_dict.keys():
            hand = Hand(player.get_bet())

            if player == 'House':
                hand.add_card(Card('Ace','Hearts',11))
                hand.add_card(Card('9','Clubs',9))
            elif i==0: #dealt to player 1
                hand.add_card(Card('Ace','Hearts',11))
                hand.add_card(Card('Ace','Clubs',11)) 
                i+=1
            elif i==1: #dealt to player 2
                hand.add_card(Card('6','Hearts',6))
                hand.add_card(Card('5','Clubs',5))

            new_hand_list = [hand]
            self.table_dict[player] = new_hand_list
                    

        print("Testing Deal complete\n")
   
    def check_dealer_blackjack(self):
        ''' Calculates dealer hand and returns T/F '''
        dealers_score = self.table_dict['House'][0].get_hand_val()
        if dealers_score == 21: 
            print ('Yikes sorry. Dealer has Blackjack...')
            return True #if dealer does have 
        else: return False #if dealer doesnt have 
  
    def balance_snapshot(self):
        ''' captures dict snapshot of players' balances for later reporting. Returns dict '''
        balance_snapshot = {} 
        for player in self.table_dict: 
            if player.get_name() == 'House': continue 
            bal = player.get_balance()
            balance_snapshot.update({player:bal}) #save point for later comparison
    
        return balance_snapshot
    
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

            #dealing 2 cards to all seats
            self.deck = Deck() #reshuffle/new deck
            # self.deal_cards()
            self.deal_cards_for_testing() ##debugging

            #players' turns
            if not self.check_dealer_blackjack():
                for player in self.table_dict.keys():
                    if player == 'House': continue #skips dealer
                    else: 
                        hand_list = self.table_dict[player]
                        played_hands = self.player_turn(player,hand_list) #returns updated hand list when done
                        self.table_dict[player] = played_hands #overwrite with played hands

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
            ans = input('Keep Playing? (y/n)').lower().strip()

            if ans == 'y' or ans == 'yes': 
                print(f'{name}, your starting balance will be ${player.get_balance()}.\n')
                #continues to next player

            elif ans == 'n' or ans == 'no': #if not playing again, $$ donated back to house
                if balance == 0:
                    print('Sorry to see you go, thanks for playing!\n')
                else: 
                    print(f'Sorry to see you go thanks for the ${balance}!\n')
                players_list.remove(player)
                #continues to next player

        except: print("I'll just pretend I understood that, you will play again\n") 
    
    if len(players_list) < max_table_size:
        players_list = build_players_list(players_list)  ##loops endlessly until reach capacity

    return players_list

def setup_table(players_list):
    '''takes in players_list of player obj, set up new table object, empty table_dict & fresh deck, returns table object '''    
    table_dict = {} #dict of player: Hand(bet) pairs, planning to replace Hand with list of Hands for splits, and handle errors dwnstream
    #create Table object, highest level container, w/ new deck
    for player in players_list:
        hand_list = []
        table_dict.update({player:hand_list}) #empty spot for everyone but Hand obj in list
    table = Table(table_dict, Deck())

    return table
    
def build_players_list(players_list):
    '''
    - Takes input from users, builds list with up to max # of players
    - returns list containing all player objects
    '''
    while len(players_list) < max_table_size: #holds up to 3 players sitting across from House
        if len(players_list) == 0: #during setup, empty list passed in
            players_list.append(Player('House',1000))  #add house with phat balance
            try:
                name = str(input("\nFirst player, choose your name.\n")).strip().lower()
                name = name.strip().lower()
                name = name[0].upper() + name[1:].lower() 

            except: pass #resets if user enters impossible str
        else:
            try:
                name = str(input("\nNext player, choose your name, or enter '*' to stop adding players.\n"))
                name = name.strip().lower()
                name = name[0].upper() + name[1:].lower() 
            except: pass #resets if user enters impossible str
        
        player = Player(name) 

        if player in players_list or player == 'House' or player == '':
            print ('Invalid Name Choice')
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
                res = player.get_name() + ':  $' + str(player.get_balance())
                print (res)            
        
            