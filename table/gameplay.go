package table

import (
	"blackjack/cards"
	"blackjack/players"
	"context"
	"fmt"
	"log/slog"
	"slices"
)

func getBetFromUser(ctx context.Context)           {}
func checkFunds(player players.Player, amount int) {}
func makeBet(player *players.Player, amount int)   {}
func (t *Table) loseBet(player *players.Player)    {}
func (t *Table) winBet(player *players.Player)     {}

func (t *Table) ResetRound() {
	for _, player := range t.Players {
		// empty all hands
		player.Hands = []cards.Hand{}
	}
	t.dealRoundStart()
}

// Deal 2 cards to each player to start the game
func (t *Table) dealRoundStart() {
	visibility := true       // draw first card face up
	for i := 0; i < 1; i++ { // deal 2 cards to each player
		for _, player := range t.Players {
			hand := player.Hands[0]
			hand.AddCard(t.Deck.DrawCard(visibility))
			player.Hands[0] = hand
		}
		t.House.Hands[0].Cards = append(t.House.Hands[0].Cards, t.Deck.DrawCard(visibility))
		visibility = false // draw 2nd card face down
	}
}

func (t Table) playerTurn(player *players.Player) {
	// func (t Table) playerTurn(player *players.Player) {
	for i := 0; i < len(player.Hands); i++ {
		hand := player.Hands[i]
		if player.CheckSplit(hand) {
			splitHands := cards.SplitHand(hand)
			for _, splitHand := range splitHands {
				// Draw one card for each
				splitHand.Cards = append(splitHand.Cards, t.Deck.DrawCard(true))
			}
			// Replace this hand in player
			player.Hands = slices.Replace(player.Hands, i, i, splitHands...)
			i-- // Replay this index
			continue
		}

	}
}

func (t Table) hitOrStick(player *players.Player) {}

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
