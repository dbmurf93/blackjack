package cards

import "fmt"

// Retrieves or calculates cached total value
func (h *Hand) GetTotalValue() int {
	if h.totalValue != nil {
		return *h.totalValue
	}

	totalValue := h.CalculateTotalValue()

	return totalValue
}

// Calculate total & cache result
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

// Checks totalValue not > 21
func (h *Hand) CheckBust() bool {
	if h.GetTotalValue() > 21 {
		fmt.Sprintln(fmt.Sprintf("Oof, %d means bust!", h.GetTotalValue()))
		return true
	}
	return false
}
