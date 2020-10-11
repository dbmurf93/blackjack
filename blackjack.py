class Player(object):
    '''  Represents a player with a name, balance, and hand_history list '''
    def __init__(self, name, balance = 50, hand_history = []):
        self.name = str(name)

    def get_name(self): 
        return self.name
    
    def get_balance(self):
        return self.balance
    
    def add_balance(self, amt):





def blackjack(self, players_list):
    '''
    Starts a new game with up to 3 players sitting across from the dealer
    Returns players_dict with updated balances
    '''



def build_players_list(self):
    '''
    - Takes input from users, builds ((dict or list)) with up to ## players
    - Each player
    '''




def check_keep_playing(self, players_list):
'''
Asks each player if they want to play again and reports their results
'''
    for player in players_list.keys():
        balance = player.get_balance()
        if balance > start_balance: 
            win_or_lose = 'win'
        elif balance == start_balance: 
            win_or_lose = 'broke even'
        elif balance < start_balance: 
            loss_amt = start_balance - balance
            win_or_lose = 'lost {loss_amt}'
        print('Good Game {player}! You {win_or_lose}.')
        ans = input('Play again? (y/n)').lower().strip()
        if ans == 'y' or ans == 'yes': continue
        elif ans == 'n' or ans == 'no':
            player_balance = get_player_balance()
            if player_balance == 0:
                print('Sorry to see you go, thanks for playing!')
            else: print('Sorry to see you go thanks for the ${player_balance}!')






if __name__ == "__main__":
    keep_playing = True
    players_dict = build_players_dict()
    
    while keep_playing:
        blackjack(players_dict)
        check_keep_playing()
        