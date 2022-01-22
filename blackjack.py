


   
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
        
            