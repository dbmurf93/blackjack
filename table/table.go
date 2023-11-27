package table

import (
	"blackjack/cards"
	"blackjack/players"
	"fmt"
)

type Table struct {
	Deck    cards.Deck
	House   players.Player
	Players map[string]players.Player
}

// Set up a new table with the provided size,
// and a "House" player with a starting balance of (100 * # of players)
func NewTable(playerMap map[string]players.Player) Table {
	return Table{
		Deck: cards.NewDeck(),
		House: players.Player{
			Balance: 100 * len(playerMap),
		},
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

	if len(t.Players) > 0 && t.House.Balance > 0 {
		return true
	}
	return false
}

func (t Table) GetBalanceSnapshot() map[string]int {
	balanceSnap := map[string]int{}
	for playerName, player := range t.Players {
		balanceSnap[playerName] = player.Balance
	}
	balanceSnap["House"] = t.House.Balance
	return balanceSnap
}

// Report whether each player won or lost this round
// & remove players with 0 balance
func (t Table) reportResults(playerNameList []string, balanceSnapshot map[string]int) {
	for _, playerName := range playerNameList {
		player := t.Players[playerName]
		playerRefBalance := balanceSnapshot[playerName]

		winAmt := player.Balance - playerRefBalance
		switch {
		case player.Balance > playerRefBalance:
			fmt.Printf("%s Won %d this round!\n", playerName, winAmt)
		case player.Balance < playerRefBalance:
			fmt.Printf("%s Lost %d this round!\n", playerName, winAmt)
		case playerRefBalance == playerRefBalance:
			fmt.Printf("%s Broke Even. Solid.\n", playerName)
		}
		if player.Balance == 0 {
			delete(t.Players, playerName)
			fmt.Printf("%s is out of the game\n", playerName)
		}
	}

}
