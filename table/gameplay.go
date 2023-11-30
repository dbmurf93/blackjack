package table

import (
	"blackjack/cards"
	"blackjack/players"
	"blackjack/utils"
	"fmt"
	"log/slog"
	"slices"
)

func (t *Table) PlayRound() {
	t.Deck.Shuffle()

	t.reset()

	balanceSnap := t.takeBalanceSnapshot()
	for _, player := range t.Players {
		err := player.SetBet()
		for err != nil {
			err = player.SetBet()
		}
	}

	for _, player := range t.Players {
		t.playerTurn(player)
	}

	t.dealerTurn()

	t.scoreTable()

	t.reportResults(balanceSnap)

}

// Returns whether any players would like to continue
// && dealer still has money
func (t Table) CheckKeepPlaying() bool {
	// Create a copy of t.Players names to iterate over
	var playerNameList []string
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

// empty all hands & deal round start
func (t *Table) reset() {
	for _, player := range t.Players {
		player.Hands = []cards.Hand{
			{
				Cards: []cards.Card{},
			},
		}
	}
	t.House.Dealer.Hands = []cards.Hand{
		{
			Cards: []cards.Card{},
		},
	}

	t.dealRoundStart()
}

// Deal 2 cards to each player to start the game
func (t *Table) dealRoundStart() {
	var hand *cards.Hand
	visibility := true       // draw first card face up
	for i := 0; i < 2; i++ { // deal 2 cards to each player
		for _, player := range t.Players {
			hand = &player.Hands[0]
			hand.AddCard(t.Deck.DrawCard(visibility))
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

// Report whether each player won or lost this round
// & remove players with 0 balance
func (t Table) reportResults(balanceSnapshot map[string]int) {
	for _, player := range t.Players {
		playerRefBalance := balanceSnapshot[player.Name]

		switch winAmt := player.Balance - playerRefBalance; {
		case winAmt > 0:
			fmt.Printf("%s Won %d this round!\nNew balance: %d", player.Name, winAmt, player.Balance)

		case winAmt < 0:
			if player.Balance == 0 {
				fmt.Printf("%s Lost everything this round!\n", player.Name)
				break
			}
			fmt.Printf("%s Lost %d this round!\nNew balance: %d", player.Name, winAmt, player.Balance)

		case winAmt == 0:
			fmt.Printf("%s Broke Even. Solid.\nBalance: %d", player.Name, player.Balance)
		}
	}
}

// Update Player balances with win/loss/wash for each of their hands based on the dealer's final score
func (t *Table) scoreTable() {
	houseHand := t.House.Dealer.Hands[0]
	houseScore := houseHand.GetTotalValue()

	for _, player := range t.Players {
		for _, playerHand := range player.Hands {
			if houseHand.IsBlackjack() {
				// automatic loss for everyone unless blackjack
				if !playerHand.IsBlackjack() {
					continue
				}
			}

			switch playerScore := playerHand.GetTotalValue(); {
			case playerScore > 21:
				// if player bust, do nothing
				// Balance adjusts when bet is made
			case houseScore > 21, houseScore < playerScore:
				// if house bust or player wins
				player.WinBet()
			case houseScore > playerScore:
				// if house beats player, do nothing
			case houseScore == playerScore:
				// if no one wins
				player.BreakEven()
			}
		}
	}
}

// Recursive func for player to hit, stick, or split on dealt hand
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
		if hand.IsBlackjack() {
			fmt.Println("Winner Winner!!")
			break
		}

		handValue := hand.GetTotalValue()
		hitMsg := fmt.Sprintf(
			"Your hand is: [Y/n]\n"+
				"%v - Value: %d\n"+
				"Would you like to hit?", hand.Show(), handValue)

		hit = utils.PromptYesOrNo(hitMsg)

		if hit {
			hand.AddCard(t.Deck.DrawCard(true))
			switch handValue = hand.GetTotalValue(); {
			case handValue > 21:
				fmt.Println(fmt.Sprintf("Oof, %d means bust!", handValue))
				done = true
				break
			case handValue == 21:
				fmt.Println("Nice! You got 21")
				done = true
				break
			}
			continue
		}
		fmt.Sprintln(fmt.Sprintf("%s has chosen to stick at %d", player.Name, handValue))
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
