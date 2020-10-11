class Player(object):
    '''  Represents a player with a name, balance, and hand_history list '''
    def __init__(self, name, balance = 50, hand_history = []):
        self.name = str(name)
        self.balance = balance
        self.hand_history = hand_history

    def get_name(self): 
        return self.name
    
    def get_balance(self):
        return self.balance
    
    def add_to_balance(self, amt):
        ''' takes amt argument as a positive int '''
        # balance = self.get_balance()
        # balance += amt
        self.balance += amt
   

    def make_bet(self, bet):
        self.balance -= bet






def blackjack(self, players_list):
    '''
    Starts a new game with up to 3 players sitting across from the dealer
    Returns players_dict with updated balances
    '''
    pass


def build_players_list(self):
    '''
    - Takes input from users, builds ((dict or list)) with up to ## players
    - Each player
    '''
    pass




def check_keep_playing(self, players_list):
    '''
    Asks each player if they want to play again, reports their results
    returns whether the game should start again, as well as whos playing
    '''
    
    for player in players_list:
        balance = player.get_balance 
        name = player.get_name()
        win_amt = balance - ref_balance
        
        if balance > ref_balance: 
            win_or_lose = 'Won ${win_amt}'

        elif balance == ref_balance: 
            win_or_lose = 'broke even.'

        elif balance < ref_balance: 
            loss = abs(win_amt)
            win_or_lose = 'lost ${loss}'

        print('{name}, You {win_or_lose} this hand.')
        ans = input('Play again? (y/n)').lower().strip()
        
        if ans == 'y' or ans == 'yes': 
            bet = int(input("Enter bet..."))
            continue #next player
        elif ans == 'n' or ans == 'no':
            player_balance = player.get_player_balance()
            if player_balance == 0:
                print('Sorry to see you go, thanks for playing!')
            else: 
                print('Sorry to see you go thanks for the ${player_balance}!')
            
            players_list.remove(player)
            continue

        else: print("I'll just pretend I understood that, you will play again")

    return players_list







if __name__ == "__main__":
    keep_playing = True
    players_list = build_players_list()
    
    while keep_playing:
        blackjack(players_list)
        players_list = check_keep_playing(players_list) #returns players list based on who wants to play again, any leftover money is donated back to house
        if len(players_list) == 0: 
            print('Bye for now!')
            break
        else: 
            print('Starting new game with {players_list}'
            continue