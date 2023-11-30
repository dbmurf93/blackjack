package players

import (
	"blackjack/utils"
	"errors"
	"fmt"
)

// Set player bet from user input
//
// TODO: clean this input better
func (p *Player) SetBet() error {
	var bet int

	switch err := utils.PromptUserForInput(fmt.Sprintf("%s - Enter a valid bet:", p.Name), &bet); {
	case err != nil:
		return err
	case bet == 0:
		return errors.New("Bet must be non-zero")
	case !p.hasEnoughFunds(bet):
		return errors.New(fmt.Sprintf("Not Enough funds. You only have %d", p.Balance))
	}

	p.Bet = bet
	p.Balance -= bet

	return nil
}

func (p Player) hasEnoughFunds(amount int) bool {
	return p.Balance >= amount
}

// Transfer double bet amount to player
func (p *Player) WinBet() {
	p.Balance += 2 * p.Bet
}

// Transfer bet amount to player
func (p *Player) BreakEven() {
	p.Balance += p.Bet
}
