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
		// Capture current state before playing a round
		balanceSnapshot := gameTable.GetBalanceSnapshot()
		gameTable.ResetRound()

		// play a round of blackjack
		// TODO

		// Update player balances and see if they want to keep playing
		keepPlaying = gameTable.CheckKeepPlaying(balanceSnapshot)
	}
	fmt.Println("Thanks for playing")
}
