package player

import (
	"fmt"
	"strings"
	"time"
	"unicode"
)

// Represents a player with a name, balance, and current bet,
type Player struct {
	Bet     int
	Balance int
	// TODO: prevent exiting and restarting to get the starting $50??
}

// Asks for name input, and for valid names,
// add player to the list with a starting balance
func BuildPlayersMap(tableMaxSize int) map[string]Player {
	var (
		players       map[string]Player
		playerCounter = 1
	)

	// TODO: Separate out name input to be more unit testable
	for len(players) < tableMaxSize {
		playerName := ""
		fmt.Printf(`
Enter player %d name
(A-z, no numbers or special characters allowed)
:
`, playerCounter)
		fmt.Scanln(&playerName)
		switch {
		case playerName == "":
			fmt.Println("No name provided, try again...")
			time.Sleep(2 * time.Second)
			continue
		case strings.ToLower(playerName) == "house":
			fmt.Println("'House' is not an allowed Name, try again...")
			time.Sleep(2 * time.Second)
			continue
		case !isLettersOnly(playerName):
			fmt.Println("Must use only letters (A-z) for player name, try again...")
			time.Sleep(2 * time.Second)
			continue
		default:
			if _, ok := players[playerName]; ok {
				fmt.Printf("%s is already at the table, choose another name", playerName)
				time.Sleep(2 * time.Second)
				continue
			}
			players[playerName] = Player{Balance: 100}

			fmt.Printf("%s was added to the table!\n", playerName)
			playerCounter++
		}
	}
	return players
}

func isLettersOnly(s string) bool {
	for _, r := range s {
		if !unicode.IsLetter(r) {
			return false
		}
	}
	return true
}
