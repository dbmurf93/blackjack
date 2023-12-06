package utils

import (
	"fmt"
	"log"
	"log/slog"
	"os"
	"strings"
)

// Loops through a list to check existence of provided item
//
// Usage:
//
//	ok := utils.ExistsInList(player, playerNameList)`
func ExistsInList[T comparable](item T, listOfT []T) bool {
	for _, i := range listOfT {
		if i == item {
			return true
		}
	}
	return false
}

func SetupLogging() {
	logfile, err := os.Create("blackjack.log")
	if err != nil {
		log.Fatal("error creating logfile", err)
	}
	defer logfile.Close()

	opts := slog.HandlerOptions{
		Level: slog.LevelDebug, // TODO set this as a param once more statements added
	}
	logger := slog.New(slog.NewJSONHandler(logfile, &opts))
	slog.SetDefault(logger)
}

// Reports to both stdout and logfile and then exits when err != nil
//
// TODO: reduce duplication in the future or parameterize this func
func LogErr(msg string, err error) {
	if err != nil {
		slog.Error(msg, err)
	}
}

// Loops prompting user with question until a Y/n response is given
//
// TODO +clean input, chan w/ ctx?
func PromptYesOrNo(question string) bool {
	ans := ""
	PromptUserForInput(question, &ans)
	switch strings.ToLower(ans) {
	case "y", "yes":
		return true
	case "n", "no":
		return false
	default:
		fmt.Printf("Invalid input: %q\nyes or no answers only\n", ans)
		return PromptYesOrNo(question)
	}
}

func PromptUserForInput[T any](question string, target *T) error {
	_, err := fmt.Println(question)
	if err != nil {
		return err
	}
	_, err = fmt.Scanln(target)
	if err != nil {
		return err
	}
	return nil
}
