package cards

import "log/slog"

type Hand struct {
	Cards     []Card
	bet       int
	completed bool
	aces      int
}

// Checks that hand length is 2 & for a pair
func (h Hand) IsSplittable() bool {
	if len(h.Cards) != 2 ||
		h.Cards[0].Name != h.Cards[1].Name {
		return false
	}
	return true
}

// Break out hand into two and return result
func SplitHand(hand Hand) []Hand {
	if !hand.IsSplittable() {
		slog.Error("", "Cannot split this hand", hand)
	}

	result := []Hand{{
		Cards: []Card{hand.Cards[0]},
	}, {
		Cards: []Card{hand.Cards[1]},
	}}
	return result
}

func addCard()         {}
func getHandValue()    {}
func getBet()          {}
func showHandAll()     {}
func showHandPartial() {}
