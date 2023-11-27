package cards

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

func addCard()         {}
func getHandValue()    {}
func getBet()          {}
func showHandAll()     {}
func showHandPartial() {}
