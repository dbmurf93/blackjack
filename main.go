package main

import (
	"fmt"
	"log/slog"

	"blackjack/players"
	"blackjack/table"
	"blackjack/utils"
)

func main() {
	fmt.Println("Welcome to BLACKJACK!")
	utils.SetupLogging()

	// setup the table
	tableMaxSize := 3

	// Get & set players
	playerMap := players.BuildPlayersMap(tableMaxSize)
	gameTable := table.NewTable(playerMap)
	slog.Info("", "Players: ", playerMap)

	keepPlaying := true
	for keepPlaying {
		// Play a round of blackjack
		gameTable.PlayRound()

		// Prompt players with money if they want to keep playing
		keepPlaying = gameTable.CheckKeepPlaying()
	}
	fmt.Println("Thanks for playing")
}
