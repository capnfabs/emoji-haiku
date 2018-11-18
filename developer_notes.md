## Build pipeline:

- Download the annotations file: https://unicode.org/repos/cldr/tags/latest/common/annotations/en.xml into `datasources/unicode-english.xml`
- Create an account here: 
  - Don't forget to create access credentials, and run `serverless config credentials --provider aws --key [key] --secret [secret]`
- serverless deploy -v && serverless invoke -f haiku -l
