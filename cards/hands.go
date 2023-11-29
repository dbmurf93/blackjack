package cards

import (
	"log/slog"
)

type Hand struct {
	Bet   int
	Cards []Card

	completed  bool `default:"false"`
	totalValue *int
}

// append card to hand & recalculate total hand value
func (h *Hand) AddCard(card Card) {
	h.Cards = append(h.Cards, card)
	h.CalculateTotalValue()
}
func (h *Hand) MarkCompleted() {
	h.completed = true
}
func (h *Hand) IsCompleted() bool {
	return h.completed
}

// True if a 2-card hand adds up to 21
func (h Hand) IsBlackjack() bool {
	return len(h.Cards) == 2 && h.GetTotalValue() == 21
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

func getBet()          {}
func showHandAll()     {}
func showHandPartial() {}
