# Emoji Haiku!

> 🌌 🏕️
>
> 🇹🇩 🖖
>
> 🎽 📛
> MILKY WAY CAMPING
>
> FLAG FOR CHAD VULCAN SALUTE
>
> RUNNING SHIRT NAME BADGE

## What?

Emoji Haiku is a small program that generates nonsense poems in a 5-7-5 syllable pattern based on
the [Unicode emoji descriptions](http://unicode.org/emoji/charts/full-emoji-list.html)
(_Warning: 46 MB page_).

## How do I use it?

Basically, `cd` into the repo and then run:

- `go run main/main.go` - outputs a single emoji haiku, using the pre-computed datasources in the
  `datasources` directory. Optionally run with `--debug`.
- `go run unicodescraper/scrape.go` - scrapes the aforementioned unicode emoji descriptions page and
  outputs a JSON format that's easier to work with.
- `go run syllablecount/syllable_count.go` - parses the [CMU pronunciation dictionary](
  https://svn.code.sf.net/p/cmusphinx/code/trunk/cmudict/) to precompute syllable counts.


## Acknowledgements
Somewhat inspired by [Haiku by Robot](https://twitter.com/haiku_by_robot), [Wizard Generator](https://twitter.com/WizardGenerator), [Aubergine Bot](https://twitter.com/AubergineBot), [Emoji Tracker](http://emojitracker.com/) and plenty of others.

With apologies to anyone who has ever put time and energy into a real poem.
