# Developer notes

Welcome, adventurer! Here's a guide to how this code works.

## Commands

- Build / run environment is managed by [Pipenv](https://github.com/pypa/pipenv). You might need to install it.
- Make a haiku on the command line with `pipenv run haiku`
- Run the tests on the command line with `pipenv run tests`
- There's type checking and pep-8 style checking, with `pipenv run typecheck` and `pipenv run stylecheck`.
- All those commands are defined in the `Pipfile`.

## Package structure

### Python code

- `emoji/`: For parsing / working with the unicode spec and rendering emojis. It's pretty application-specific, but you might learn a trick or two about how Unicode works from it!
- `haiku.py`: For generating emoji haikus.
- `syllables.py`: For counting syllables in a string.
- `api/`: All the stuff that interacts with web services, e.g. AWS Lambda. You can ignore this if you're just generating Haikus on the command line.
- `tests/`: Woah, yes! Tests! They're not super comprehensive, but `pipenv run tests` will run them.

### Other stuff

`datasources/` is where a downloaded set of data sources is kept. This is:
- files from the unicode spec.
    - `emoji-unicode-11/` contains a dump of this directory: [unicode.org/Public/emoji/11.0/](https://unicode.org/Public/emoji/11.0/).
      - According to their FTP server, this was last modified 2018-02-07.
      - I downloaded it 2018-11-19.
    - `unicode-english.xml` is the English language unicode CLDR localization datasource, downloaded from [here](https://unicode.org/repos/cldr/tags/latest/common/annotations/en.xml)
      - Note that there's some emoji that _aren't_ in this file - notably, flags and keycaps. They're in [this file](https://www.unicode.org/repos/cldr/tags/latest/common/annotationsDerived/en.xml) instead.
  - The CMU pronunciation dictionary, which I modified a little, in order to remove some dodgy pronunciations. Download the original [here](http://www.speech.cs.cmu.edu/cgi-bin/cmudict).

## Deploy to AWS lambda?

- This gets done with `serverless`! Which I think is a silly name for a framework. Let's see if it works.
- Set up your credentials from Amazon Web Services (because you can host this on AWS Lambda): `serverless config credentials --provider aws --key [key] --secret [secret]`
- You'll probably need to install the plugins using `serverless plugin install --name serverless-prune-plugin && serverless plugin install --name serverless-python-requirements` (see the `severless.yml` for plugin names; this all uses npm under the hood)
- You can deploy it with `serverless deploy -v`
  - To deploy to production, add `--stage production`
- After deploy, check it works with `serverless invoke -f haiku -l`
  - This is "invoke `-f`unction haiku `-l`ogs"
  - If something isn't working, `serverless.yml` is where the config is at.
  - Remove old versions with `sls prune -n 0 --stage [dev|production]`

### Tweeter credentials

If you want to set up tweeting every 6 hours, you need to add twitter configuration variables. These are stored in `twitter-config.json`, which is in `.gitignore`, so you probably won't have this file on your machine when you checkout the code. Here's what to do:

- `cp twitter-config.json.template twitter-config.json`
- Create a new app, and get the config values from the [Twitter Developer Site](https://developer.twitter.com/en/apps)
- Fill them in
- You should be good to go.
- (Note to self - if you lose this file - check the emojihaikus account in 1password).


## References / resources I used on the way

Here's everything you might need to know about the unicode spec.

- Latest CLDR english annotations: https://unicode.org/repos/cldr/tags/latest/common/annotations/en.xml
- Latest CLDR _derived_ english annotations (includes variants): https://unicode.org/repos/cldr/tags/latest/common/annotationsDerived/en.xml
- There's a note here about 'standardised variants': http://www.unicode.org/Public/7.0.0/ucd/StandardizedVariants.html. Some emoji require adding a suffix of `\uFE0F` in order to get the emoji-style string; without it, they render as outlines / [dingbats](https://en.wiktionary.org/wiki/dingbat#Etymology).
- Full emoji list: https://unicode.org/emoji/charts/full-emoji-list.html.
  - I think a previous version of Emoji Haiku parsed this file.
- The official emoji spec: http://www.unicode.org/reports/tr51/tr51-14.html (this is the latest published version as per this commit, corresponding to Unicode 11.)
- According to spec, valid unicode codepoints are from 0x0 to 0x10FFFF (see http://unicode.org/glossary/#code_point).


# TODO / possible enhancements
- **[refactor]** Rework the way we distinguish between gendered emojis. Goodness gracious; there's so many if/else statements here. They're not really the same thing, they just implement the same interface.
- **[emoji]** We're missing flags and families. I don't know if they're super necessary, but I sorta liked the flags in v1.
- **[language]** Maybe Re-gender some of the words, some of the time.
  - I think it adds flavour for the verbs - Maybe add something that randomly changes 'person running' to 'man running' and 'woman running'.
  - I'm pretty keen to keep the professions non-gendered.
  - I'd love to actually use merman / mermaid in addition to merperson 🧜‍♂️ 🧜‍♀️
- **[api]** Support supplying a gender or a skin color as an HTTP arg and having that applied consistently to everyone in the haiku.
- **[haikus]** Maybe modify the weights so that it favours nature and people, and less symbols. I'd want to go digging more into the philosophy behind Haikus for this, though.


# Stuff to talk about in a blog post

- Stuff that's happened since I wrote the first Emoji Haiku:
  - Multiple versions of the Emoji Spec!
  - Apple changed the pistol to a water gun.
  - People started to become more observant about how weird emoji names sound on twitter, thanks to [Kai on Twitter](https://twitter.com/kai_wanders/status/1013386281408192513):
    - Apologies to people looking at Emoji Haiku on a screen reader.
    - Note also that people who historically haven't used screen-readers are now affected by this too, e.g. [in-car reading of text messages](https://www.theguardian.com/lifeandstyle/2018/dec/08/tim-dowling-hallucinating-wife-talking-to-car)
- I originally thought that gendering was either SIGN MODE or OBJECT MODE. Turns out OBJECT MODE is _really really complicated_, and isn't really a mode, but actually an entirely different way of thinking. The official spec treating them very differently should have probably been a hint for this. There's probably something interesting to talk about here, though I haven't distilled _what_ exactly.
- It's super hard to get these details right:
  - Edge bug: https://developer.microsoft.com/en-us/microsoft-edge/platform/issues/13583622/
  - Chrome on OSX (possibly other) platforms where rendering doesn't work correctly on ZWJ sequences without setting the font correctly.
    -  Compare Woman Zombie on Emojipedia, which renders correctly: https://emojipedia.org/woman-zombie/
  - Adding a MEN WITH RABBIT EARS emoji 👯‍♂️to my Twitter handle broke my blog rendering due to an encoding issue. Wow. I don't even _know_ who is at fault for this.
