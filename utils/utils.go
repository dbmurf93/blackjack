package utils

import (
	"log/slog"
	"os"
)

// Generic func to check existence of an item in a list
// Ex:
//
//	`ok := utils.ExistsInList(player, playerNameList)`
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
	HandleErr("error creating logfile", err)
	defer logfile.Close()

	opts := slog.HandlerOptions{
		Level: slog.LevelDebug,
	}
	logger := slog.New(slog.NewJSONHandler(logfile, &opts))
	slog.SetDefault(logger)
}

func HandleErr(msg string, err error) {
	if err != nil {
		slog.Error(msg, err)
	}
}
