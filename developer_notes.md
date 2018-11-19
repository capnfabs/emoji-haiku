## Build pipeline:

- Download some data sources: 
  - The CLDR latest english XML file. Note that this is used as the source of truth for what constitutes a valid emoji! If there's stuff in here that's in pre-release versions of the spec, it's going to cause compatability issues. If this causes major problems, consider filtering it by something in the official 'machine-readable' files associated with the unicode spec. 
    - Here's the CLDR localization datasource for english: https://unicode.org/repos/cldr/tags/latest/common/annotations/en.xml. Save that as `datasources/unicode-english.xml`.
    - If you later need to cross-reference it to (e.g.) version 11 of the unicode spec, here's the official files: https://unicode.org/Public/emoji/11.0/
    - There's a lot of emojis that won't turn up using this datasource: notably, keycaps and flags. Use this source instead, if that's important to you: https://www.unicode.org/repos/cldr/tags/latest/common/annotationsDerived/en.xml
- Create an account here: 
  - Don't forget to create access credentials, and run `serverless config credentials --provider aws --key [key] --secret [secret]`
- serverless deploy -v && serverless invoke -f haiku -l


## References

Here's everything you might need to know about the unicode spec.
- Latest CLDR english annotations: https://unicode.org/repos/cldr/tags/latest/common/annotations/en.xml
- Latest CLDR _derived_ english annotations (includes variants): https://unicode.org/repos/cldr/tags/latest/common/annotationsDerived/en.xml

There's a note here about 'standardised variants': http://www.unicode.org/Public/7.0.0/ucd/StandardizedVariants.html. Some emoji require adding a suffix of \uFE0F in order to get the emoji-style string; without it, they render as outlines / dingbats.

Full emoji list:
- https://unicode.org/emoji/charts/full-emoji-list.html
