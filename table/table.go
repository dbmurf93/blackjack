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

// Capture status of all players & house balance
func (t Table) takeBalanceSnapshot() map[string]int {
	balanceSnap := map[string]int{}

	for playerName, player := range t.Players {
		balanceSnap[playerName] = player.Balance
	}
	balanceSnap["House"] = t.House.Dealer.Balance

	return balanceSnap
}

// Prompt user if they have money left
// Delete from Table if user doesn't opt in or is out of money
func (t *Table) promptToKeepPlaying(player players.Player) {
	keepPlaying := false

	if player.Balance > 0 {
		keepPlaying = utils.PromptYesOrNo("Would you like to keep playing? [Y/n]\n")
	}

	if !keepPlaying {
		delete(t.Players, player.Name)
		fmt.Printf("%s is out of the game\n", player.Name)
	}
}
