package cards

import (
	"math/rand"
	"time"
)

type Card struct {
	Name       string
	Suit       string
	Value      int
	visibility bool `default:"true"`
}

func (c Card) DisplayCard(card Card) string {
	if card.visibility {
		return card.Name + " of " + card.Suit
	}
	return "[]"
}

type Deck struct {
	cards       []Card
	drawCounter int
}

func NewDeck() Deck {
	cardNames := []string{"2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King", "Ace"}
	cardValues := []int{2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11}
	suits := []string{"Hearts", "Diamonds", "Clubs", "Spades"}
	newDeck := Deck{}
	for _, suit := range suits {
		for i, name := range cardNames {
			newDeck.cards = append(newDeck.cards, Card{
				Name:  name,
				Suit:  suit,
				Value: cardValues[i],
			})
		}
	}
	newDeck.Shuffle()
	return newDeck
}

// Shuffle cards and
func (d Deck) Shuffle() {
	// TODO consider using crypto/rand for source?
	// could hide the extra processing time with an animation
	rand.New(rand.NewSource(time.Now().UnixNano()))
	rand.Shuffle(len(d.cards), func(i, j int) { d.cards[i], d.cards[j] = d.cards[j], d.cards[i] })
	d.drawCounter = 0
}

func (d Deck) DrawCard(visibility bool) Card {
	if d.drawCounter > len(d.cards)-1 {
		d.Shuffle()
	}
	drawCard := d.cards[d.drawCounter]
	drawCard.visibility = visibility

	d.drawCounter++

	return drawCard
}
