package table

import "blackjack/player"

type Table struct {
	MaxSize int
	Players []player.Player
}

// Set up a new table with the provided size, and a "House" player with a starting balance
func NewTable(tableSize int) Table {
	return Table{
		MaxSize: tableSize,
		Players: []player.Player{
			{
				Balance: 1000,
				Name:    "House",
			},
		},
	}
}
