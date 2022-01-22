from typing import 

def setup_table(players_list):
    '''takes in players_list, set up new table object, empty table_dict & fresh deck, returns table object '''    
    table_dict = {} #dict of player: Hand(bet) pairs, planning to replace Hand with list of Hands for splits, and handle errors dwnstream
    # creates Table object, highest level container, w/ new deck
    for player in players_list:
        hand_list = []
        table_dict.update({player:hand_list}) #empty spot for everyone but Hand obj in list
    table = Table(table_dict, Deck())

    return table


def check_for_split(self, player, hand) -> bool:
    ''' checks cards, checks player funds, asks player if appropriate, returns T/F '''
    ans='' 
    # if split is possible.. 
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
            