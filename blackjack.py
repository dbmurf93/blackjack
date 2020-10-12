import random


class Player(object):
    '''  Represents a player with a name, balance, and current bet'''
    def __init__(self, name, balance = 50, bet = 0):
        self.name = str(name)
        self.balance = balance
        self.bet = bet

    def __str__(self):
        return self.name
    
    def __repr__(self):
        return (self.name, self.balance)

    def __hash__(self):
        return self.name.__hash__()

    def get_name(self): 
        return self.name
    
    def get_balance(self):
        return self.balance
   
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


class Card(object):
    '''
    Represents card object with name & suit, as strings
    value: int for calculation, tuple for Ace
    '''
    def __init__(self, name, suit, value):
        self.name = name
        self.suit = suit
        self.value = value

    def get_value(self):
        return self.value
    
    def __str__(self):
        return self.name + ' of ' + self.suit #ex: Ace of Spades, King of Hearts
        
    def __repr__(self):
        if self.name == '10':
            return (self.name + self.suit[0]) 
        else: 
            return (self.name[0] + self.suit[0]) #ex: AS, KH

    def __hash__(self):
        return self.repr.__hash__()
   

class Deck(object):
    '''
    Represents 
    1) reference list of card objects, 
    2) list to be shuffled and drawn from, 
    3) self-contained discard pile list.
    '''
    def __init__(self):
        self.ref_deck = []

        card_names = ['Ace','1','2','3','4','5','6','7','8','9','10','Jack','Queen','King']
        card_vals = [(1,10),1,2,3,4,5,6,7,8,9,10,10,10,10]

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

        

def build_players_list(): #currently pre-filled in
    '''
    - Takes input from users, builds ((dict or list)) with up to ## players
    - returns players_list containing player objects
    '''
    players_list = []

    #name = str(input("Enter Player 1 name: "))
    name = 'DylanM'
    players_list.append(Player(name)) 
    print(f'Hello and welcome {name}, your starting balance is $50.')

    while len(players_list) < 2: ##change max game size here##
        #name = str(input("Enter next player name: "))
        name = 'KevMcSnatch'
        players_list.append(Player(name)) #creates player object in slot
        print(f'Hello and welcome {name}, your starting balance is $50.')
        
    return players_list


def play_blackjack(players_list):
    '''
    Starts a new game, repeats until no bets placed or 'quit' command entered
    Returns players_list when done
    '''
    #shuffle deck
    deck = Deck()
    deck = deck.new_shuffle()
    house = Player('TheHouse',1000)
    table = [house] #list of who's getting cards
    for player in players_list:
        table.append(player.get_name())
    print ("Table:", table)

    #deal cards
    pass
    #for player in players_list:
        #deal until stop or bust, with option to split if same faced card
    
    
    """ while True:
                try:
                    bet = int(input("Enter an integer bet...")) 
                    while bet > balance: 
                        try: bet = int(input('Enter a bet you can afford...your poor family...get help man you have a problem.'))
                        except: pass
                    break
                except: pass #keeps looping while incorrect input type

            player.make_bet(bet) #saves bet and moves on to next player"""





def check_keep_playing(players_list, player_balances):
    '''
    Asks each player if they want to play again, reports their results
    returns whos playing next as new players_list
    '''
    iteration_list = players_list.copy()
    for player in iteration_list: #reports score and asks to play again, removes players not playing
        ref_balance = player_balances[player] #balance before this round started
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
        ans = input('Play again? (y/n)').lower().strip()
        
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

        else: print("I'll just pretend I understood that, you will play again") ##ADD FUNCTION HERE## for better input control, same for name choosing.
    
    ##could add option here to add new players if list isn't at capacity.##
    return players_list


#################
#################


if __name__ == "__main__":
    keep_playing = True
    players_list = build_players_list()
    house_acct = 1000000 #if you win a million bucks in this game you should win something
    
    while keep_playing == True: #Keeps playing until bets stop
        balance_snapshot = {} 
        for player in players_list: #captures dict snapshot before playing
            balance = player.get_balance()
            balance_snapshot.update({player:balance})

        play_blackjack(players_list) #deals to players and dealer, changes player balances, repeats until no bets given

        players_list = check_keep_playing(players_list, balance_snapshot) #edits&returns players list based on who wants to play again, any leftover money is donated back to house...naturally.

        if len(players_list) == 0: #exit program when empty table
            print('Bye for now!')
            keep_playing == False
        else: 
            playing = []
            for x in players_list: playing.append(str(x))
            print(f'Starting new game with {playing[:-1]} and {playing[-1:]}')
            