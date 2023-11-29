package table

import (
	"blackjack/cards"
	"blackjack/players"
	"blackjack/utils"
	"context"
	"fmt"
	"log/slog"
	"slices"
)

func getBetFromUser(ctx context.Context)                {}
func checkFunds(player players.Player, amount int) bool { return false }

func makeBet(player *players.Player, amount int) {
	player.Bet = amount
}
func (t *Table) loseBet(player *players.Player) {
	player.Balance -= player.Bet
}
func (t *Table) winBet(player *players.Player) {
	player.Balance += player.Bet
}

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
		t.House.Dealer.Hands[0].Cards = append(t.House.Dealer.Hands[0].Cards, t.Deck.DrawCard(visibility))
		visibility = false // draw 2nd card face down
	}
}

func (t *Table) dealerTurn() {
	house := t.House
	dealerHand := house.Dealer.Hands[0]
	dealerHandValue := func() int { return dealerHand.GetTotalValue() }

	if dealerHandValue() == 21 {
		house.blackjack = true
		fmt.Println("Dealer has blackjack, too bad!")
	}

	// Dealer hits for anything under 17
	for dealerHandValue() < 17 {
		dealerHand.AddCard(t.Deck.DrawCard(true))
		if dealerHandValue() >= 21 {
			break
		}
	}

	fmt.Printf("Dealer finishes at %d\n", dealerHandValue())
}

func (t *Table) CheckScores() {
	houseScore := t.House.Dealer.Hands[0].GetTotalValue()
	switch {
	case houseScore > 21:
		// Everyone wins
	case t.House.blackjack:
		// No one wins
	}

	for _, player := range t.Players {
		for _, hand := range player.Hands {
			playerScore := hand.GetTotalValue()
			switch {
			case houseScore > playerScore:
				// house wins
			case houseScore < playerScore:
				// player wins
			case houseScore == playerScore:
				// no one wins
			}
		}
	}
}

func (t Table) playerTurn(player *players.Player) error {
	for handIndex, hand := range player.Hands {
		if hand.IsCompleted() {
			continue
		}
		if player.CheckSplit(hand) {
			splitHands := cards.SplitHand(hand)
			for _, splitHand := range splitHands {
				// Draw one card for each
				splitHand.Cards = append(splitHand.Cards, t.Deck.DrawCard(true))
			}
			// Replace this hand in player
			player.Hands = slices.Replace(player.Hands, handIndex, handIndex, splitHands...)

			// play remaining hands & end turn
			return t.playerTurn(player)
		}

		t.hitOrStick(player, &hand)

		// update player hand
		player.Hands[handIndex] = hand
	}
	return nil
}

// Prompt user for hit and draw accordingly until a "no" response or bust
func (t Table) hitOrStick(player *players.Player, hand *cards.Hand) {
	var (
		done, hit bool
	)

	for !done {
		handValue := hand.GetTotalValue()
		hit = utils.PromptYesOrNo(
			fmt.Sprintf(
				"Your hand is: [Y/n]\n"+
					"%v - Value: %d\n"+
					"Would you like to hit?", hand, handValue))
		if hit {
			hand.AddCard(t.Deck.DrawCard(true))
			if bust := hand.CheckBust(); bust {
				break
			}
			continue
		}
		fmt.Sprintln(fmt.Sprintf("%s has chosen to stick at %d", player.Name, hand.GetTotalValue()))
		done = true
	}

	hand.MarkCompleted()
}

// ee
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
