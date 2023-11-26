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
	Name    string
	// TODO: prevent exiting and restarting to get the starting $50
}

// Asks for name input, and for valid names,
// add player to the list with a starting balance
func BuildPlayersList(players []Player, tableMaxSize int) []Player {
	// TODO: Separate out name input to be more unit testable
	for len(players) < tableMaxSize {
		playerName := ""
		fmt.Printf(`
Enter your player name: 
(A-z, no numbers or special characters allowed)

`)
		fmt.Scanln(&playerName)
		switch {
		case playerName == "":
			fmt.Printf("No name provided, try again...")
			time.Sleep(2 * time.Second)
			continue
		case strings.ToLower(playerName) == "house":
			fmt.Printf("'House' is not an allowed Name, try again...")
			time.Sleep(2 * time.Second)
			continue
		case !isLettersOnly(playerName):
			fmt.Printf("Must use only letters (A-z) for player name, try again...")
			time.Sleep(2 * time.Second)
			continue
		default:
			if alreadyExists(playerName, players) {
				continue
			}
			players = append(players, Player{
				Balance: 100,
				Name:    playerName,
			})
			fmt.Printf("%s was added to the table!", playerName)
		}
	}
	return players
}

func alreadyExists(name string, players []Player) bool {
	for _, player := range players {
		if name == player.Name {
			fmt.Printf("%s is already at the table, choose another name", name)
			time.Sleep(2 * time.Second)
			return true
		}
	}
	return false
}

func isLettersOnly(s string) bool {
	for _, r := range s {
		if !unicode.IsLetter(r) {
			return false
		}
	}
	return true
}
