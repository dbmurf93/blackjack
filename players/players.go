package players

import (
	"blackjack/cards"
	"blackjack/utils"
	"fmt"
	"strings"
	"time"
	"unicode"
)

// Represents a player with a name, balance, and current bet,
type Player struct {
	Bet     int
	Balance int
	Hands   []cards.Hand // players can have multiple hands per round if there is a split
}

func (p *Player) CheckSplit(hand cards.Hand) bool {
	if !hand.IsSplittable() {
		return false
	}

	confirmSplit := utils.ProcessYesOrNo(
		fmt.Sprintf("Do you want to split this hand: [Y/n]\n%v\n", hand))

	if confirmSplit {
		return true
	}
	return false
}

// Asks for name input, and for valid names,
// add player to the list with a starting balance
//
// TODO: Separate out name input to be more unit testable
func BuildPlayersMap(tableMaxSize int) map[string]Player {
	var (
		players       = make(map[string]Player)
		playerCounter = 1
	)

	for len(players) < tableMaxSize {
		playerName := ""
		fmt.Printf("Enter player %d name\n"+
			"\t(- A-z, no numbers or special characters allowed\n"+
			"\t - Leave empty to continue with the current players)\n", playerCounter)
		fmt.Scanln(&playerName)
		if playerName == "" {
			fmt.Println("No name provided, let's play!")
			break
		}
		switch {
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
			fmt.Println("Current Players:")
			for playerName := range players {
				fmt.Printf("\t%s\n", playerName)
			}
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
