package table

import (
	"blackjack/players"
	"errors"
	"fmt"
)

func makeBet(player *players.Player, amount int) error {
	if checkFunds(*player, amount) {
		player.Bet = amount
		return nil
	}
	return errors.New(fmt.Sprintf("Insufficient funds\nHave: %d Need: %d", player.Balance, amount))
}

func checkFunds(player players.Player, amount int) bool {
	return player.Balance >= amount
}

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
