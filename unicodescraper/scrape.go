package main

import (
	"encoding/json"
	"fmt"
	"os"
	"strconv"
	"strings"

	"github.com/PuerkitoBio/goquery"
	"github.com/capnfabs/emojihaiku/emojihaiku"
)

func main() {
	doc, err := goquery.NewDocument("http://unicode.org/emoji/charts/full-emoji-list.html")
	if err != nil {
		panic(err)
	}
	tbody := doc.Find("tbody").First()
	chars := tbody.Find("td.chars")
	list := make([]emojihaiku.Emoji, chars.Length())
	for i := 0; i < chars.Length(); i++ {
		elem := chars.Eq(i)
		names := elem.Parent().Find("td.name")
		year, _ := strconv.ParseInt(trimNonNumeric(elem.Parent().Find("td.age").Text()), 10, 32)
		list[i] = emojihaiku.Emoji{
			Emoji:        elem.Text(),
			Descriptions: trimAll(strings.Split(names.Eq(0).Text(), "≊")),
			Tags:         trimAll(strings.Split(names.Eq(1).Text(), ",")),
			Year:         int(year),
			DispMode:     elem.Parent().Find("td.default").Text(),
		}
	}
	bytes, err := json.MarshalIndent(list, "", "  ")
	if err != nil {
		panic(err)
	}
	os.Stdout.Write(bytes)
	fmt.Println()
}

func trimAll(ss []string) []string {
	ret := make([]string, len(ss))
	for i, s := range ss {
		// Trim spaces, lowercase, replace "smart quote" apostrophes with real ones.
		ret[i] = strings.Replace(strings.ToLower(strings.TrimSpace(s)), "’", "'", -1)
	}
	return ret
}

func trimNonNumeric(s string) string {
	del := strings.Trim(s, "0123456789")
	return strings.Trim(strings.TrimSpace(s), del)
}
