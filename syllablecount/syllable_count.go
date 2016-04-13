package main

import (
	"bufio"
	"encoding/json"
	"fmt"
	"os"
	"regexp"
	"strings"

	"github.com/capnfabs/emojihaiku/emojihaiku"
)

var variantSuffix = regexp.MustCompile(`\(\d\)$`)

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
	// map of words to syllable counts, so we can dedupe for different pronounciations but same
	// syllable counts.
	// variants are included as WORD(variant)
	ws := make(map[string][]int)
	for scanner.Scan() {
		tok := strings.Split(scanner.Text(), " ")
		// Comment
		if tok[0] == ";;;" {
			continue
		}
		// Otherwise, first token is word, each subsequent is a sound.
		word := tok[0]
		loc := variantSuffix.FindStringIndex(word)
		if loc != nil {
			word = word[:loc[0]]
		}
		syllables := 0
		for _, sound := range tok[1:] {
			// There are different variants of each sound so we need to trim the number off the end.
			s := strings.Trim(sound, "01234567890")
			if _, ok := soundDict[s]; ok {
				syllables++
			}
		}
		if shouldAdd(ws, word, syllables) {
			list = append(list, emojihaiku.WordSyl{
				Word:      word,
				Syllables: syllables,
			})
			ws[word] = append(ws[word], syllables)
		}
	}
	bytes, err := json.MarshalIndent(list, "", "  ")
	if err != nil {
		panic(err)
	}
	os.Stdout.Write(bytes)
	fmt.Println()
}

func shouldAdd(ws map[string][]int, word string, syllables int) bool {
	_, ok := ws[word]
	if !ok {
		return true
	}
	for _, variant := range ws[word] {
		if variant == syllables {
			// this syllable count already exists for this word.
			return false
		}
	}
	return true
}
