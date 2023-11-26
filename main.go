package main

import (
	"fmt"

	"blackjack/player"
	"blackjack/table"
)

func main() {
	fmt.Println("Welcome to BLACKJACK!")
	tableSize := 4
	gameTable := table.NewTable(tableSize)
	playersList := player.BuildPlayersList(gameTable.Players, gameTable.MaxSize)
	fmt.Print(playersList)
}
