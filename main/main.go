package main

import (
	"encoding/json"
	"flag"
	"fmt"
	"io/ioutil"
	"math/rand"
	"regexp"
	"strings"
	"time"

	"github.com/capnfabs/emojihaiku/emojihaiku"
)

var debug = flag.Bool("debug", false, "Turn on debug output")

func loadJSON(file string, v interface{}) {
	bytes, err := ioutil.ReadFile(file)
	if err != nil {
		panic(err)
	}
	err = json.Unmarshal(bytes, v)
	if err != nil {
		panic(err)
	}
}

type descEmoji struct {
	desc     string
	emoji    emojihaiku.Emoji
	sylCount int
}

var emoji []emojihaiku.Emoji
var sylCountByWord map[string]int
var emojiBySylCount [][]descEmoji

var notLettersRegex = regexp.MustCompile("[^a-zA-Z]")

func main() {
	flag.Parse()
	rand.Seed(time.Now().UnixNano())
	loadJSON("datasources/emoji.json", &emoji)
	var syllablecount []emojihaiku.WordSyl
	loadJSON("datasources/syllablecount.json", &syllablecount)
	sylCountByWord := make(map[string]int)
	for _, sylcount := range syllablecount {
		sylCountByWord[sylcount.Word] = sylcount.Syllables
	}

	emojiBySylCountInc := buildEmojiBySylCountTable(emoji, sylCountByWord)
	emojiBySylCount = buildCumTable(emojiBySylCountInc)
	if *debug {
		for i := 0; i < len(emojiBySylCount); i++ {
			fmt.Printf("%d syllables, %d words\n", i, len(emojiBySylCount[i]))
		}
	}

	var used []string

	pattern := []int{5, 7, 5}

	emojiLines := make([]string, len(pattern))
	descLines := make([]string, len(pattern))

	for idx, syl := range pattern {
		emojiLines[idx], descLines[idx] = generateLine(syl, &used)
	}

	fmt.Println(strings.Join(emojiLines, "\n"))
	fmt.Println(strings.ToUpper(strings.Join(descLines, "\n")))
}

func buildEmojiBySylCountTable(emojis []emojihaiku.Emoji, sylCountByWord map[string]int) map[int][]descEmoji {
	ret := make(map[int][]descEmoji)
	for _, emoji := range emojis {
		for _, desc := range emoji.Descriptions {
			sylcount, err := countSyllables(sylCountByWord, desc)
			if err != nil {
				// Don't use this word
				continue
			}
			set, ok := ret[sylcount]
			if !ok {
				set = make([]descEmoji, 0)
			}
			set = append(set, descEmoji{
				desc:     desc,
				emoji:    emoji,
				sylCount: sylcount,
			})
			ret[sylcount] = set
		}
	}
	return ret
}

func countSyllables(sylCountByWord map[string]int, desc string) (int, error) {
	// All substrings.
	words := notLettersRegex.Split(desc, -1)
	sylcount := 0
	for _, word := range words {
		if len(notLettersRegex.ReplaceAllString(word, "")) == 0 {
			// This is a blank string for the purposes of pronunciation.
			continue
		}
		wordSyls, ok := sylCountByWord[strings.ToUpper(word)]
		if !ok {
			if *debug {
				fmt.Println("Couldn't find word", word)
			}
			return 0, fmt.Errorf("Couldn't find word %s", word)
		}
		sylcount += wordSyls
	}
	return sylcount, nil
}

func buildCumTable(table map[int][]descEmoji) [][]descEmoji {
	maxKey := maxKey(table)
	ret := make([][]descEmoji, maxKey+1)
	// Don't allow zero-syllable, but init it.
	ret[0] = make([]descEmoji, 0)
	// Each loop iteration appends the map entry for that number of syllables to the set from the
	// previous iteration.
	for i := 1; i <= maxKey; i++ {
		val, ok := table[i]
		if ok {
			ret[i] = val
		} else {
			ret[i] = make([]descEmoji, 0)
		}
		ret[i] = append(ret[i], ret[i-1]...)
		if *debug {
			// Print the first emoji from each set as a sanity check.
			fmt.Println(ret[i][0])
		}
	}
	return ret
}

func maxKey(vals map[int][]descEmoji) int {
	// unsigned
	max := 0
	for k := range vals {
		if k > max {
			max = k
		}
	}
	return max
}

func generateLine(sylCount int, used *[]string) (string, string) {
	var emojis []string
	var descs []string
	for i := sylCount; i > 0; {
		// Choose an emoji at random
		space := emojiBySylCount[i]
		e := space[rand.Int31n(int32(len(space)))]
		emojis = append(emojis, e.emoji.Emoji)
		descs = append(descs, e.desc)
		i -= e.sylCount
		//computeSyllableCount[e.Descriptions]
	}
	return strings.Join(emojis, " "), strings.ToUpper(strings.Join(descs, " "))
}
