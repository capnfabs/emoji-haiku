package main

import (
	"bufio"
	"encoding/json"
	"fmt"
	"os"
	"strings"

	"github.com/capnfabs/emojihaiku/emojihaiku"
)

func buildSoundDict() map[string]struct{} {
	vowels := make(map[string]struct{})
	f, err := os.Open("datasources/cmudict-0.7b.phones.txt")
	if err != nil {
		panic(err)
	}
	scanner := bufio.NewScanner(f)
	for scanner.Scan() {
		tok := strings.Split(scanner.Text(), "\t")
		if tok[1] == "vowel" {
			vowels[tok[0]] = struct{}{}
		}
	}
	return vowels
}

func main() {
	soundDict := buildSoundDict()

	f, err := os.Open("datasources/cmudict-0.7b.txt")
	if err != nil {
		panic(err)
	}
	scanner := bufio.NewScanner(f)
	var list []emojihaiku.WordSyl
	for scanner.Scan() {
		tok := strings.Split(scanner.Text(), " ")
		// Comment
		if tok[0] == ";;;" {
			continue
		}
		// Otherwise, first token is word, each subsequent is a sound.
		syllables := 0
		for _, sound := range tok[1:] {
			// There are different variants of each sound so we need to trim the number off the end.
			s := strings.Trim(sound, "01234567890")
			if _, ok := soundDict[s]; ok {
				syllables++
			}
		}
		list = append(list, emojihaiku.WordSyl{
			Word:      tok[0],
			Syllables: syllables,
		})
	}
	bytes, err := json.MarshalIndent(list, "", "  ")
	if err != nil {
		panic(err)
	}
	os.Stdout.Write(bytes)
	fmt.Println()
}
