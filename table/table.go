package table

import (
	"blackjack/cards"
	"blackjack/players"
	"blackjack/utils"
	"fmt"
)

type House struct {
	Dealer    players.Player
	blackjack bool
}

type Table struct {
	Deck    cards.Deck
	House   House
	Players map[string]players.Player
}

// Set up a new table with the provided size,
// and a "House" player with a starting balance of (100 * # of players)
func NewTable(playerMap map[string]players.Player) Table {
	return Table{
		Deck: cards.NewDeck(),
		House: House{
			Dealer: players.Player{
				Balance: 100 * len(playerMap),
			}},
		Players: playerMap,
	}
}

// This runs after each round:
// - tally wins & losses
// - remove players with 0 balances
// continue if any survivors & house still has money
func (t Table) CheckKeepPlaying(balanceSnapshot map[string]int) bool {
	var playerList []string
	// Create a copy of t.Players names to iterate over
	for playerName := range t.Players {
		playerList = append(playerList, playerName)
	}

	t.reportResults(playerList, balanceSnapshot)

	if len(t.Players) > 0 && t.House.Dealer.Balance > 0 {
		return true
	}
	return false
}

func (t Table) GetBalanceSnapshot() map[string]int {
	balanceSnap := map[string]int{}
	for playerName, player := range t.Players {
		balanceSnap[playerName] = player.Balance
	}
	balanceSnap["House"] = t.House.Dealer.Balance
	return balanceSnap
}

// Report whether each player won or lost this round
// & remove players with 0 balance
func (t Table) reportResults(playerNameList []string, balanceSnapshot map[string]int) {
	for _, playerName := range playerNameList {
		keepPlaying := true
		player := t.Players[playerName]
		playerRefBalance := balanceSnapshot[playerName]

		switch winAmt := player.Balance - playerRefBalance; {
		case winAmt > 0:
			fmt.Printf("%s Won %d this round!\nNew balance: %d", playerName, winAmt, player.Balance)
		case winAmt < 0:
			if player.Balance == 0 {
				keepPlaying = false
				fmt.Printf("%s Lost everything this round!\n", playerName)
				continue
			}
			fmt.Printf("%s Lost %d this round!\nNew balance: %d", playerName, winAmt, player.Balance)
		case winAmt == 0:
			fmt.Printf("%s Broke Even. Solid.\nBalance: %d", playerName, player.Balance)
		}

		// prompt user if they have money left
		if player.Balance > 0 {
			keepPlaying = utils.PromptYesOrNo("Would you like to keep playing? [Y/n]\n")
		}
		// If user doesn't opt in
		if !keepPlaying {
			delete(t.Players, playerName)
			fmt.Printf("%s is out of the game\n", playerName)
		}
	}
}
