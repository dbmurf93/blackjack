package main

import (
	"fmt"

	"blackjack/player"
	"blackjack/table"
)

func main() {
	fmt.Println("Welcome to BLACKJACK!")

	// setup the table
	tableSize := 4
	gameTable := table.NewTable(tableSize)
	playersList := player.BuildPlayersMap(gameTable.MaxSize)
	gameTable.Players = playersList
	fmt.Println(playersList)

	keepPlaying := true
	for keepPlaying {
		// Capture current state before playing a round
		balanceSnapshot := gameTable.GetBalanceSnapshot()

		// play a round of blackjack
		// TODO

		// Update player balances and see if they want to keep playing
		keepPlaying = gameTable.CheckKeepPlaying(balanceSnapshot)
	}
	fmt.Println("Thanks for playing")
}
