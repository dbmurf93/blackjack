package cards

import (
	"fmt"
	"log/slog"
)

type Hand struct {
	Cards []Card
	Bet   int

	bust       bool `default:"false"`
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

// Checks totalValue not > 21
func (h *Hand) CheckBust() bool {
	if h.GetTotalValue() > 21 {
		fmt.Sprintln(fmt.Sprintf("Oof, %d means bust!", h.GetTotalValue()))
		h.bust = true
		return true
	}
	return false
}

func (h *Hand) GetTotalValue() int {
	if h.totalValue != nil {
		return *h.totalValue
	}

	totalValue := h.CalculateTotalValue()

	return totalValue
}

// calculate total & cache result
func (h *Hand) CalculateTotalValue() int {
	aceCounter := 0
	totalValue := 0

	for _, card := range h.Cards {
		if card.Name == "Ace" {
			aceCounter++
		}
		totalValue += card.Value
	}

	for totalValue > 21 && aceCounter > 0 {
		aceCounter--
		totalValue -= 10
	}

	// cache & return result
	h.totalValue = &totalValue
	h.CheckBust()

	return totalValue
}

func getBet()          {}
func showHandAll()     {}
func showHandPartial() {}
