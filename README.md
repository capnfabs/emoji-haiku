# Emoji Haiku!

> 🌌 🏕️<br>
> 🇹🇩 🖖<br>
> 🎽 📛
>
> MILKY WAY CAMPING <br>
> FLAG FOR CHAD VULCAN SALUTE <br>
> RUNNING SHIRT NAME BADGE

## What?

Emoji Haiku is a small program that generates nonsense poems in a 5-7-5 syllable pattern based on
the [Unicode emoji descriptions](http://unicode.org/emoji/charts/full-emoji-list.html)
(_Warning: 46 MB page_).

## How do I use it?

Head to http://capnfabs.net/emoji-haiku.

Alternatively, here's a quick overview of the code:

- `go run unicodescraper/scrape.go` - scrapes the aforementioned unicode emoji descriptions page and
  outputs a JSON format that's easier to work with.
- `go run syllablecount/syllable_count.go` - parses the [CMU pronunciation dictionary](
  https://svn.code.sf.net/p/cmusphinx/code/trunk/cmudict/) to precompute syllable counts. Note that I've commented out some words from the CMU dictionary stored in the `datasources` directory; I'll be darned before "national" or "fuel" are two-syllable words.
- `java/` - this aptly-named directory is a Java gradle project. It does two things:
  - 1. `./gradlew run`: runs the program locally and generates a single Emoji Haiku
  - 2. `./gradlew buildAwsZip`: builds a ZIP file that you can upload to AWS and use as a lambda function (see [developer_notes.md](developer_notes.md) for more info).

There's more samples [here](samples.md).

## Acknowledgements
Somewhat inspired by [Haiku by Robot](https://twitter.com/haiku_by_robot), [Wizard Generator](https://twitter.com/WizardGenerator), [Aubergine Bot](https://twitter.com/AubergineBot), [Emoji Tracker](http://emojitracker.com/) and plenty of others.

With apologies to anyone who has ever put time and energy into a real poem.
