package table

import (
	"blackjack/players"
)

// Transfer bet amount from player to Dealer
func (t *Table) loseBet(player *players.Player) {
	player.Balance -= player.Bet
	t.House.Dealer.Balance += player.Bet
}

// Transfer bet amount from Dealer to player
func (t *Table) winBet(player *players.Player) {
	player.Balance += player.Bet
	t.House.Dealer.Balance -= player.Bet
}
