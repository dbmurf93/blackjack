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
	Players map[string]*players.Player
}

// Set up a new table with the provided size,
// and a "House" player with a starting balance of (100 * # of players)
func NewTable(playerMap map[string]*players.Player) Table {
	return Table{
		Deck: cards.NewDeck(),
		House: House{
			Dealer: players.Player{
				Balance: 100 * len(playerMap),
			}},
		Players: playerMap,
	}
}

// Returns whether any players would like to continue
// && dealer still has money
func (t *Table) CheckKeepPlaying() bool {
	var playerNameList []string
	// Create a copy of t.Players names to iterate over
	for playerName := range t.Players {
		playerNameList = append(playerNameList, playerName)
	}
	for _, playerName := range playerNameList {
		t.promptToKeepPlaying(t.Players[playerName])
	}
	if len(t.Players) > 0 {
		return true
	}
	return false
}

// Prompt user if they have money left
// Delete from Table if user doesn't opt in or is out of money
func (t *Table) promptToKeepPlaying(player *players.Player) {
	keepPlaying := false

	if player.Balance > 0 {
		keepPlaying = utils.PromptYesOrNo(player.Name + " - " + "Would you like to keep playing? [Y/n]\n")
	}

	if !keepPlaying {
		delete(t.Players, player.Name)
		fmt.Printf("%s is out of the game\n", player.Name)
	}
}
