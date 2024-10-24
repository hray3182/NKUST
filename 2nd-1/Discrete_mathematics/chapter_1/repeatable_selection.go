package main

import "fmt"

func main() {
	elems := []string{"a", "b", "c"}
	combinations := RepeatableSelection(elems, 4)
	for _, e := range combinations {
		fmt.Println(e)
	}
}

// 列出所有排列組合，從elems中選出n個元素，可重複選取
// 例如：elems = ["a", "b", "c"]，n = 3，則返回 ["aaa", "aab", "aac", "aba", "abb", "abc", "aca", "acb", "acc", "baa", "bab", "bac", "bba", "bbb", "bbc", "bca", "bcb", "bcc", "caa", "cab", "cac", "cba", "cbb", "cbc", "cca", "ccb", "ccc"]
func RepeatableSelection(elems []string, n int) []string {
	return repeatableSelectionHelper(elems, n, "")
}

func repeatableSelectionHelper(elems []string, length int, current string) []string {
	if length == 0 {
		return []string{current}
	}

	var result []string
	for _, elem := range elems {
		result = append(result, repeatableSelectionHelper(elems, length-1, current+elem)...)
	}
	return result
}
