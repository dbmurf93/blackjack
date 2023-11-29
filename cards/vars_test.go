package cards_test

import "blackjack/cards"

// Testing hands
var (
	// A A A
	acesX3 = cards.Hand{

		Cards: []cards.Card{
			{
				Name:  "Ace",
				Value: 11,
				Suit:  "Diamonds",
			}, {
				Name:  "Ace",
				Value: 11,
				Suit:  "Spades",
			}, {
				Name:  "Ace",
				Value: 11,
				Suit:  "Clubs",
			},
		},
	}

	// A J
	blackjack = cards.Hand{
		Cards: []cards.Card{
			{
				Name:  "Ace",
				Value: 11,
				Suit:  "Diamonds",
			}, {
				Name:  "Jack",
				Value: 10,
				Suit:  "Diamonds",
			},
		},
	}

	// 2 2
	twos = cards.Hand{
		Cards: []cards.Card{
			{
				Name:  "2",
				Value: 2,
				Suit:  "Diamonds",
			}, {
				Name:  "2",
				Value: 2,
				Suit:  "Diamonds",
			},
		},
	}

	// 8 10 4
	bust = cards.Hand{
		Cards: []cards.Card{
			{
				Name:  "8",
				Value: 8,
			},
			{
				Name:  "10",
				Value: 10,
			},
			{
				Name:  "4",
				Value: 4,
			},
		},
	}

	// 8 10 3
	nailedIt = cards.Hand{
		Cards: []cards.Card{
			{
				Name:  "8",
				Value: 8,
			},
			{
				Name:  "10",
				Value: 10,
			},
			{
				Name:  "3",
				Value: 3,
			},
		},
	}
)
