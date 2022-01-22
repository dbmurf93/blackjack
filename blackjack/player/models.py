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

