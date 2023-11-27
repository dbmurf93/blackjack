package table

import (
	"blackjack/cards"
	"blackjack/players"
	"context"
	"fmt"
	"log/slog"
)

func getBetFromUser(ctx context.Context)           {}
func checkFunds(player players.Player, amount int) {}
func makeBet(player *players.Player, amount int)   {}
func (t *Table) loseBet(player *players.Player)    {}
func (t *Table) winBet(player *players.Player)     {}
func (t *Table) DealAll() {
	visibility := true       // draw first card face up
	for i := 0; i < 1; i++ { // deal 2 cards to each player
		for _, player := range t.Players {
			hand := player.Hands[0]
			hand.Cards = append(hand.Cards, t.Deck.DrawCard(visibility))
			player.Hands[0] = hand
		}
		visibility = false
	}
}

func (t Table) playerTurn(player *players.Player) {
	hand := player.Hands[0]
	if player.CheckSplit(hand) {
		// if hand split is available & approved by user
		player.Hands = cards.SplitHand(hand)

	}
}

func splitHint(hand cards.Hand) {
	if !hand.IsSplittable() {
		slog.Warn("", "Cannot split this hand", hand)
	}
	switch hand.Cards[0].Value {
	case 11, 8:
		fmt.Println("You should split this hand")
	case 4, 5, 10:
		fmt.Println("You should NOT split this hand")
	case 2, 3, 7:
		fmt.Println("You should split this hand if the dealer shows 7 or lower")
	case 6:
		fmt.Println("You should split this hand if the dealer shows a 2-6")
	case 9:
		fmt.Println("You should split this hand if the dealer shows 2-6, 8, or 9")
	}
}
