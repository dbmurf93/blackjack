package utils

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
