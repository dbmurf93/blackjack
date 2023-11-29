package cards_test

import (
	"blackjack/cards"
	"testing"
)

func TestHandGetTotalValue(t *testing.T) {

	tests := []struct {
		expected int
		hand     cards.Hand
	}{
		{13, acesX3},
		{21, blackjack},
		{22, bust},
		{21, nailedIt},
	}

	for _, test := range tests {
		totalValue := test.hand.GetTotalValue()
		if totalValue != int(test.expected) {
			t.Fatalf("Wanted %d Got %d", test.expected, totalValue)
		}
	}
}

func TestIsSplittable(t *testing.T) {
	tests := []struct {
		hand           cards.Hand
		expectedResult bool
	}{
		{blackjack, false},
		{acesX3, false},
		{twos, true},
	}
	for _, test := range tests {
		result := test.hand.IsSplittable()
		if result != test.expectedResult {
			t.Fatalf("\nincorrect split result '%t' for hand:\n %+v\nExpected '%t'", result, test.hand, test.expectedResult)
		}
	}
}
